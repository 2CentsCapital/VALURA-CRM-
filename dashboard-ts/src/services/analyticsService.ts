
import { FreshworksService } from './freshworksService';
function normalizeName(name: string) {
  return name.trim().toLowerCase().replace(/\s+/g, ' ');
}

export class AnalyticsService {
  static async getContactsBySource(pipelineId?: string) {
    const contactsResp = await FreshworksService.getAllContacts(1, 100);
    const contacts = contactsResp.contacts || [];
    const deals = await FreshworksService.getAllDealsPaginated();
    const filteredDeals = pipelineId ? deals.filter((d) => d.deal_pipeline_id == pipelineId) : deals;

    // Build a map of normalized deal names to their sales account names
    const dealNameToSource: Record<string, string> = {};
    for (const deal of filteredDeals) {
      const dealName = normalizeName(deal.name || '');
      // Priority 1: Get sales account name
      if (deal.sales_account_id) {
        // Note: For performance, you may want to cache sales account lookups
        // Here, we just use the ID as a placeholder
        dealNameToSource[dealName] = String(deal.sales_account_id);
      } else if (deal.deal_stage && deal.deal_stage.name) {
        const stageName = deal.deal_stage.name.toLowerCase();
        if (/(walk|online|referral|reference|lead)/.test(stageName)) {
          dealNameToSource[dealName] = deal.deal_stage.name;
        }
      }
    }

    // Group contacts by source
    const grouped: Record<string, any[]> = {};
    for (const contact of contacts) {
      const firstName = (contact.first_name || '').trim();
      const lastName = (contact.last_name || '').trim();
      const fullName = `${firstName} ${lastName}`.trim();
      const fullNameNorm = normalizeName(fullName);
      // Priority 1: tags
      if (contact.tags && contact.tags.length > 0) {
        for (const tag of contact.tags) {
          if (!grouped[tag]) grouped[tag] = [];
          grouped[tag].push(contact);
        }
        continue;
      }
      // Priority 2: match contact to deal by name
      let matchedSource: string | null = null;
      if (dealNameToSource[fullNameNorm]) {
        matchedSource = dealNameToSource[fullNameNorm];
      } else {
        for (const [dealName, source] of Object.entries(dealNameToSource)) {
          if (fullNameNorm && (dealName.includes(fullNameNorm) || fullNameNorm.includes(dealName))) {
            matchedSource = source;
            break;
          }
        }
      }
      if (matchedSource) {
        if (!grouped[matchedSource]) grouped[matchedSource] = [];
        grouped[matchedSource].push(contact);
      } else {
        if (!grouped['No Source']) grouped['No Source'] = [];
        grouped['No Source'].push(contact);
      }
    }
    return grouped;
  }

  static async getContactsNotInOpportunities(pipelineId?: string) {
    const contactsResp = await FreshworksService.getAllContacts(1, 100);
    const contacts: any[] = contactsResp.contacts || [];
    const deals = await FreshworksService.getAllDealsPaginated();
    const filteredDeals = pipelineId ? deals.filter((d) => d.deal_pipeline_id == pipelineId) : deals;
    // Build a set of normalized deal names for fast lookup
    const normalizedDealNames = new Set(filteredDeals.map((d: any) => normalizeName(d.name || '')));
    // Filter contacts whose normalized full name does not match any deal name
    const contactsWithoutDeals = contacts.filter((contact: any) => {
      const firstName = (contact.first_name || '').trim();
      const lastName = (contact.last_name || '').trim();
      const fullName = `${firstName} ${lastName}`.trim();
      const fullNameNorm = normalizeName(fullName);
      return !normalizedDealNames.has(fullNameNorm);
    });
    return contactsWithoutDeals;
  }

  static async getDashboardSummary(pipelineId?: string) {
    const contactsResp = await FreshworksService.getAllContacts(1, 100);
    const contacts = contactsResp.contacts || [];
    const deals = await FreshworksService.getAllDealsPaginated();
    const filteredDeals = pipelineId ? deals.filter((d) => d.deal_pipeline_id == pipelineId) : deals;
    const contactsWithoutOpportunities = await this.getContactsNotInOpportunities(pipelineId);
    const sourcesGrouped = await this.getContactsBySource(pipelineId);
    const totalOpportunityValue = filteredDeals.reduce((sum, d) => sum + (parseFloat(d.amount || '0') || 0), 0);
    // Stage distribution
    const stageStats: Record<string, { count: number; total_value: number }> = {};
    for (const deal of filteredDeals) {
      const stageName = deal.deal_stage && deal.deal_stage.name ? deal.deal_stage.name : 'Unknown';
      if (!stageStats[stageName]) stageStats[stageName] = { count: 0, total_value: 0 };
      stageStats[stageName].count++;
      stageStats[stageName].total_value += parseFloat(deal.amount || '0') || 0;
    }
    const topStages = Object.entries(stageStats)
      .map(([stage, stats]) => ({ stage, ...stats }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
    // Owner distribution
    const ownerStats: Record<string, { count: number; total_value: number }> = {};
    for (const deal of filteredDeals) {
      let ownerName = 'Unassigned';
      if (deal.owner && typeof deal.owner === 'object') {
        ownerName = deal.owner.display_name || deal.owner.email || `Owner ${deal.owner.id}`;
      }
      if (!ownerStats[ownerName]) ownerStats[ownerName] = { count: 0, total_value: 0 };
      ownerStats[ownerName].count++;
      ownerStats[ownerName].total_value += parseFloat(deal.amount || '0') || 0;
    }
    const topOwners = Object.entries(ownerStats)
      .map(([owner, stats]) => ({ owner, ...stats }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
    // Sources breakdown
    const sourcesBreakdown: Record<string, number> = {};
    for (const [source, arr] of Object.entries(sourcesGrouped)) {
      sourcesBreakdown[source] = arr.length;
    }
    return {
      total_contacts: contacts.length,
      total_opportunities: filteredDeals.length,
      contacts_without_opportunities: contactsWithoutOpportunities.length,
      total_opportunity_value: totalOpportunityValue,
      sources_breakdown: sourcesBreakdown,
      top_stages: topStages,
      top_owners: topOwners,
    };
  }
}

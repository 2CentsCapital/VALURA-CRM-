import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

const DOMAIN = process.env.FRESHWORKS_DOMAIN;
const API_KEY = process.env.FRESHWORKS_API_KEY;
const CONTACTS_VIEW_ID = process.env.CONTACTS_VIEW_ID || '402014829835';
const DEALS_VIEW_ID = process.env.DEALS_VIEW_ID || '402014829847';

const BASE_URL = `https://${DOMAIN}.myfreshworks.com/crm/sales/api`;

const headers = {
  'Authorization': `Token token=${API_KEY}`,
  'Content-Type': 'application/json',
};

export class FreshworksService {
  static async makeRequest(endpoint: string, params: any = {}) {
    const url = `${BASE_URL}/${endpoint}`;
    const response = await axios.get(url, { headers, params });
    return response.data;
  }

  static async getAllContacts(page = 1, per_page = 25, view_id?: string) {
    const endpoint = `contacts/view/${view_id || CONTACTS_VIEW_ID}`;
    return this.makeRequest(endpoint, { page, per_page });
  }

  static async getAllDeals(page = 1, per_page = 25, view_id?: string, include = 'owner,sales_account') {
    const endpoint = `deals/view/${view_id || DEALS_VIEW_ID}`;
    return this.makeRequest(endpoint, { page, per_page, include });
  }

  static async getAllDealsPaginated(maxPages = 100) {
    let allDeals: any[] = [];
    let page = 1;
    while (page <= maxPages) {
      const result = await this.getAllDeals(page, 100);
      const deals = result.deals || [];
      if (!deals.length) break;
      allDeals = allDeals.concat(deals);
      const meta = result.meta || {};
      if (page >= (meta.total_pages || 1)) break;
      page++;
    }
    return allDeals;
  }

  static async getDealStages() {
    const result = await this.makeRequest('selector/deal_stages');
    return result.deal_stages || [];
  }

  static async getSalesAccount(accountId: string) {
    const result = await this.makeRequest(`sales_accounts/${accountId}`);
    return result.sales_account;
  }

  static async getPipelines() {
    const result = await this.makeRequest('selector/deal_pipelines');
    return result.deal_pipelines || [];
  }
}

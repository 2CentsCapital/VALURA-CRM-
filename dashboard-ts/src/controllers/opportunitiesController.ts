import { Request, Response } from 'express';
import { FreshworksService } from '../services/freshworksService';
import { AnalyticsService } from '../services/analyticsService';

export async function getAllOpportunities(req: Request, res: Response) {
  const page = parseInt(req.query.page as string) || 1;
  const per_page = parseInt(req.query.per_page as string) || 25;
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    let data = await FreshworksService.getAllDeals(page, per_page);
    let deals = data.deals || [];
    if (pipelineId) deals = deals.filter((d: any) => d.deal_pipeline_id == pipelineId);
    res.json({ success: true, data: deals, meta: data.meta || {} });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

export async function getOpportunitiesByStage(req: Request, res: Response) {
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    // TODO: Implement grouping by stage
    res.json({ success: true, data: {}, message: 'Not implemented' });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

export async function getLeadsBySalesOwner(req: Request, res: Response) {
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    // TODO: Implement grouping by sales owner
    res.json({ success: true, data: {}, message: 'Not implemented' });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

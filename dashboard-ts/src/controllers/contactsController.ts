import { Request, Response } from 'express';
import { FreshworksService } from '../services/freshworksService';
import { AnalyticsService } from '../services/analyticsService';

export async function getAllContacts(req: Request, res: Response) {
  const page = parseInt(req.query.page as string) || 1;
  const per_page = parseInt(req.query.per_page as string) || 25;
  try {
    const data = await FreshworksService.getAllContacts(page, per_page);
    res.json({ success: true, data: data.contacts || [], meta: data.meta || {} });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

export async function getContactsBySource(req: Request, res: Response) {
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    const data = await AnalyticsService.getContactsBySource(pipelineId);
    res.json({ success: true, data });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

export async function getContactsNotInOpportunities(req: Request, res: Response) {
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    const data = await AnalyticsService.getContactsNotInOpportunities(pipelineId);
    res.json({ success: true, data });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

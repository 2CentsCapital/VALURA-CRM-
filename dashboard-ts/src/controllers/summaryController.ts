import { Request, Response } from 'express';
import { AnalyticsService } from '../services/analyticsService';

export async function getDashboardSummary(req: Request, res: Response) {
  const pipelineId = req.query.pipeline_id as string | undefined;
  try {
    const data = await AnalyticsService.getDashboardSummary(pipelineId);
    res.json({ success: true, data });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

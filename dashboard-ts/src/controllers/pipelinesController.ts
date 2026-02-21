import { Request, Response } from 'express';
import { FreshworksService } from '../services/freshworksService';

export async function getAllPipelines(req: Request, res: Response) {
  try {
    const pipelines = await FreshworksService.getPipelines();
    res.json({ success: true, data: pipelines });
  } catch (e) {
    res.status(500).json({ success: false, error: (e as Error).message });
  }
}

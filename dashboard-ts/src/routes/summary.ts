import { Router } from 'express';
import { getDashboardSummary } from '../controllers/summaryController';

const router = Router();

router.get('/', getDashboardSummary);

export default router;

import { Router } from 'express';
import { getAllOpportunities, getOpportunitiesByStage, getLeadsBySalesOwner } from '../controllers/opportunitiesController';

const router = Router();

router.get('/', getAllOpportunities);
router.get('/by-stage', getOpportunitiesByStage);
router.get('/leads-by-sales-owner', getLeadsBySalesOwner);

export default router;

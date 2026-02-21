import { Router } from 'express';
import { getAllPipelines } from '../controllers/pipelinesController';

const router = Router();

router.get('/', getAllPipelines);

export default router;

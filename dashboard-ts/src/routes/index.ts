
import { Router } from 'express';
import contactsRouter from './contacts';
import opportunitiesRouter from './opportunities';
import summaryRouter from './summary';
import pipelinesRouter from './pipelines';

const router = Router();

router.use('/contacts', contactsRouter);
router.use('/opportunities', opportunitiesRouter);
router.use('/summary', summaryRouter);
router.use('/pipelines', pipelinesRouter);

export default router;

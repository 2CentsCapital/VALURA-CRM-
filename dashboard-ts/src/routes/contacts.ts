import { Router } from 'express';
import { getAllContacts, getContactsBySource, getContactsNotInOpportunities } from '../controllers/contactsController';

const router = Router();

router.get('/', getAllContacts);
router.get('/by-source', getContactsBySource);
router.get('/not-in-opportunities', getContactsNotInOpportunities);

export default router;

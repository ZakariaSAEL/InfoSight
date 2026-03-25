import { openDB } from 'idb';

const DB_NAME = 'InfoSightDB';
const STORE_NAME = 'invoices';
const DB_VERSION = 1;

export async function initDB() {
  return openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: 'id' });
        store.createIndex('date', 'date');
        store.createIndex('vendor', 'vendor');
      }
    },
  });
}

export async function saveInvoice(invoiceData) {
  const db = await initDB();
  return db.put(STORE_NAME, invoiceData);
}

export async function getAllInvoices() {
  const db = await initDB();
  return db.getAllFromIndex(STORE_NAME, 'date');
}

export async function getInvoice(id) {
  const db = await initDB();
  return db.get(STORE_NAME, id);
}

export async function deleteInvoice(id) {
  const db = await initDB();
  return db.delete(STORE_NAME, id);
}

export async function clearAllInvoices() {
  const db = await initDB();
  return db.clear(STORE_NAME);
}

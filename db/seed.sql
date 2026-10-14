-- Enterprise Digital Banking Baseline Seed Data

INSERT OR IGNORE INTO users (id, full_name, email, password_hash, role)
VALUES ('usr_001', 'Jane Doe', 'admin@bank.com', 'password123', 'admin');

INSERT OR IGNORE INTO accounts (id, user_id, account_number, account_name, account_type, currency, available_balance, ledger_balance, status)
VALUES 
('acc_001', 'usr_001', '1002-4820-9912', 'Main Operating Account', 'Checking', 'USD', 248500.50, 250000.00, 'ACTIVE'),
('acc_002', 'usr_001', '1002-8831-4401', 'Treasury & Reserve Account', 'Savings', 'USD', 1250000.00, 1250000.00, 'ACTIVE'),
('acc_003', 'usr_001', '1002-9900-1122', 'Payroll Escrow Account', 'Escrow', 'USD', 85000.00, 85000.00, 'ACTIVE');

INSERT OR IGNORE INTO transactions (id, account_id, date, description, type, amount, running_balance, status)
VALUES
('tx_001', 'acc_001', '2026-10-12 14:22:00', 'Supplier Wire Settlement - Cloud Infra', 'DEBIT', -12450.00, 248500.50, 'COMPLETED'),
('tx_002', 'acc_001', '2026-10-11 09:15:00', 'Client Inbound Payment - Acme Corp', 'CREDIT', 45000.00, 260950.50, 'COMPLETED'),
('tx_003', 'acc_001', '2026-10-10 16:40:00', 'Payroll Batch Execution Oct-W2', 'DEBIT', -38200.00, 215950.50, 'COMPLETED'),
('tx_004', 'acc_001', '2026-10-09 11:05:00', 'Merchant POS Settlement Terminal #4', 'CREDIT', 18250.00, 254150.50, 'COMPLETED');

INSERT OR IGNORE INTO cards (id, user_id, card_holder, card_number_masked, card_type, status, monthly_limit, pos_limit, expiry_date)
VALUES
('crd_001', 'usr_001', 'Jane Doe', '•••• •••• •••• 9876', 'Executive Corporate Visa', 'ACTIVE', 25000.00, 10000.00, '12/29'),
('crd_002', 'usr_001', 'Alex Smith', '•••• •••• •••• 4421', 'Commercial Procurement Card', 'LOCKED', 15000.00, 5000.00, '08/28');

INSERT OR IGNORE INTO transfers (id, reference_number, user_id, from_account_id, to_account_id, amount, transfer_type, memo, idempotency_key, status)
VALUES
('tr_001', 'TRF-20261012-001', 'usr_001', 'acc_001', 'acc_002', 25000.00, 'Internal Transfer', 'Quarterly Treasury Rebalance', 'idem_seed_001', 'COMPLETED');

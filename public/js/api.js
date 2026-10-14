// Enterprise Digital Banking API Client
const API_BASE = '/api/v1';

const BankingAPI = {
  async getHealth() {
    const res = await fetch('/health');
    return res.json();
  },

  async login(email, password, rememberMe = false) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, remember_me: rememberMe })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async getDashboardSummary() {
    const res = await fetch(`${API_BASE}/dashboard/summary`);
    if (!res.ok) throw new Error('Failed to load dashboard summary');
    return res.json();
  },

  async getAccounts() {
    const res = await fetch(`${API_BASE}/accounts`);
    if (!res.ok) throw new Error('Failed to load accounts');
    return res.json();
  },

  async getAccountDetail(accountId) {
    const res = await fetch(`${API_BASE}/accounts/${accountId}`);
    if (!res.ok) throw new Error(`Failed to load account ${accountId}`);
    return res.json();
  },

  async getAccountTransactions(accountId) {
    const res = await fetch(`${API_BASE}/accounts/${accountId}/transactions`);
    if (!res.ok) throw new Error('Failed to load transactions');
    return res.json();
  },

  async getAccountStatement(accountId) {
    const res = await fetch(`${API_BASE}/accounts/${accountId}/statement`);
    if (!res.ok) throw new Error('Failed to generate statement');
    return res.json();
  },

  async initiateTransfer(fromAccountId, toAccountId, amount, transferType = 'Internal Transfer', memo = '', idempotencyKey = null) {
    const res = await fetch(`${API_BASE}/transfers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from_account_id: fromAccountId,
        to_account_id: toAccountId,
        amount: parseFloat(amount),
        transfer_type: transferType,
        memo: memo,
        idempotency_key: idempotencyKey || 'idem_' + Date.now()
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Transfer failed' }));
      throw new Error(err.detail || 'Transfer failed');
    }
    return res.json();
  },

  async getTransfers() {
    const res = await fetch(`${API_BASE}/transfers`);
    if (!res.ok) throw new Error('Failed to load transfers');
    return res.json();
  },

  async getCards() {
    const res = await fetch(`${API_BASE}/cards`);
    if (!res.ok) throw new Error('Failed to load cards');
    return res.json();
  },

  async toggleCardStatus(cardId, status) {
    const res = await fetch(`${API_BASE}/cards/${cardId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Status update failed' }));
      throw new Error(err.detail || 'Status update failed');
    }
    return res.json();
  },

  async updateCardLimits(cardId, monthlyLimit, posLimit) {
    const res = await fetch(`${API_BASE}/cards/${cardId}/limits`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        monthly_limit: parseFloat(monthlyLimit),
        pos_limit: parseFloat(posLimit)
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Limit update failed' }));
      throw new Error(err.detail || 'Limit update failed');
    }
    return res.json();
  },

  async submitOnboarding(companyName, fullName, workEmail, idDoc = '', addressDoc = '') {
    const res = await fetch(`${API_BASE}/onboarding`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        company_name: companyName,
        full_name: fullName,
        work_email: workEmail,
        id_document: idDoc,
        address_document: addressDoc
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Onboarding failed' }));
      throw new Error(err.detail || 'Onboarding failed');
    }
    return res.json();
  }
};

window.BankingAPI = BankingAPI;

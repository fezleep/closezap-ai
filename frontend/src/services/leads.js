const API_BASE_URL = '/api';

// Map frontend status to backend status
const STATUS_MAP = {
  'new': 'new',
  'contacted': 'engaged',
  'qualified': 'engaged',
  'converted': 'closed',
  'lost': 'closed',
};

// Map backend status to frontend status
const REVERSE_STATUS_MAP = {
  'new': 'new',
  'engaged': 'contacted',
  'closed': 'converted',
};

export const leadsService = {
  async getAll() {
    const response = await fetch(`${API_BASE_URL}/leads`);
    if (!response.ok) {
      throw new Error('Failed to fetch leads');
    }
    const leads = await response.json();
    // Transform backend status to frontend status
    return leads.map(lead => ({
      ...lead,
      status: REVERSE_STATUS_MAP[lead.status] || lead.status,
      lastMessage: lead.last_message,
      lastContactAt: lead.last_contact_at,
    }));
  },

  async updateStatus(id, status) {
    const backendStatus = STATUS_MAP[status] || status;
    const response = await fetch(`${API_BASE_URL}/leads/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: backendStatus }),
    });
    if (!response.ok) {
      throw new Error('Failed to update lead status');
    }
    const updated = await response.json();
    return {
      ...updated,
      status: REVERSE_STATUS_MAP[updated.status] || updated.status,
      lastMessage: updated.last_message,
      lastContactAt: updated.last_contact_at,
    };
  },
};

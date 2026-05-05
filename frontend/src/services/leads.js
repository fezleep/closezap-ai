const API_BASE_URL = 'http://localhost:8000/api';

function normalizeLead(lead) {
  return {
    ...lead,
    lastMessage: lead.last_message,
    lastContactAt: lead.last_contact_at,
  };
}

export const leadsService = {
  async getAll() {
    const response = await fetch(`${API_BASE_URL}/leads`);

    if (!response.ok) {
      throw new Error('failed to fetch leads');
    }

    const leads = await response.json();
    return leads.map(normalizeLead);
  },

  async create(data) {
    const response = await fetch(`${API_BASE_URL}/leads/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('failed to create lead');
    }

    const lead = await response.json();
    return normalizeLead(lead);
  },

  async close(id) {
    const response = await fetch(`${API_BASE_URL}/leads/${id}/close`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('failed to close lead');
    }

    const lead = await response.json();
    return normalizeLead(lead);
  },
};

export async function closeLead(leadId) {
  return leadsService.close(leadId);
}
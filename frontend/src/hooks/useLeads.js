import { useState, useEffect, useCallback } from 'react';
import { leadsService } from '../services/leads';

export function useLeads() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLeads = useCallback(async () => {
    try {
      setLoading(true);
      const data = await leadsService.getAll();
      setLeads(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateLeadStatus = useCallback(async (id, status) => {
    try {
      await leadsService.updateStatus(id, status);
      setLeads(prev => prev.map(lead =>
        lead.id === id ? { ...lead, status } : lead
      ));
    } catch (err) {
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);

  return { leads, loading, error, fetchLeads, updateLeadStatus };
}

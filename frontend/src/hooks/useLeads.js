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

  const createLead = useCallback(async (payload) => {
    const createdLead = await leadsService.create(payload);
    setLeads((prev) => [
      { ...createdLead, _highlight: true },
      ...prev,
    ]);
    return createdLead;
  }, []);

  const closeLead = useCallback(async (id) => {
    const updatedLead = await leadsService.close(id);

    setLeads((prev) =>
      prev.map((lead) => (lead.id === id ? updatedLead : lead))
    );

    return updatedLead;
  }, []);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);

  return {
    leads,
    loading,
    error,
    fetchLeads,
    createLead,
    closeLead,
  };
}
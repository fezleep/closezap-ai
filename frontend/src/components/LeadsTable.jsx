import { closeLead, generateReply } from '../services/leads';
import { useState } from 'react';

export function LeadsTable({ leads, onCloseLead }) {

  const [aiReply, setAiReply] = useState(null);
  const [loadingReply, setLoadingReply] = useState(false);

  const truncateMessage = (message, maxLength = 55) => {
    if (!message) return '-';
    if (message.length <= maxLength) return message;
    return message.substring(0, maxLength) + '...';
  };

  const getStatusBadge = (status) => {
    const styles = {
      new: 'border-white/15 text-zinc-300 bg-white/5',
      engaged: 'border-[#d4af37]/30 text-[#d4af37] bg-[#d4af37]/10',
      closed: 'border-white/10 text-white bg-white/10',
    };

    return (
      <span
        className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${
          styles[status] || 'border-white/10 text-zinc-400 bg-white/5'
        }`}
      >
        {status}
      </span>
    );
  };

  const getIntentText = (intent) => {
    const styles = {
      hot: 'text-[#d4af37]',
      warm: 'text-zinc-300',
      cold: 'text-zinc-500',
    };

    return (
      <span className={`text-sm font-medium ${styles[intent] || 'text-zinc-500'}`}>
        {intent || '-'}
      </span>
    );
  };

  const handleClose = async (id) => {
    try {
      await onCloseLead(id);
    } catch (error) {
      console.error('error closing lead', error);
    }
  };

  if (!leads || leads.length === 0) {
    return (
      <div className="py-16 text-center">
        <h3 className="text-sm font-medium text-white">no leads yet</h3>
        <p className="mt-2 text-sm text-zinc-500">
          create a lead to start testing the flow
        </p>
      </div>
    );
  }

  const handleGenerateReply = async (lead) => {
  try {
    setLoadingReply(true);

    const data = await generateReply(
      lead.id,
      lead.lastMessage || "hello"
    );

    setAiReply({
      leadName: lead.name,
      text: data.reply
    });

  } catch (error) {
    console.error("error generating reply", error);
  } finally {
    setLoadingReply(false);
  }
};

return (
  <>
    <div className="overflow-hidden rounded-2xl border border-white/10">
      <table className="min-w-full divide-y divide-white/10">
        <thead className="bg-black/20">
          <tr>
            <th className="px-5 py-4 text-left text-xs text-zinc-500">lead</th>
            <th className="px-5 py-4 text-left text-xs text-zinc-500">interest</th>
            <th className="px-5 py-4 text-left text-xs text-zinc-500">status</th>
            <th className="px-5 py-4 text-left text-xs text-zinc-500">intent</th>
            <th className="px-5 py-4 text-left text-xs text-zinc-500">last message</th>
            <th className="px-5 py-4 text-right text-xs text-zinc-500">action</th>
          </tr>
        </thead>

        <tbody className="divide-y divide-white/10 bg-[#111111]">
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td className="px-5 py-5">{lead.name}</td>

              <td className="px-5 py-5">{lead.interest}</td>

              <td className="px-5 py-5">{lead.status}</td>

              <td className="px-5 py-5">{lead.intent}</td>

              <td className="px-5 py-5">
                {lead.lastMessage || '-'}
              </td>

              <td className="px-5 py-5 text-right">
                <button
                  onClick={() => handleGenerateReply(lead)}
                  className="ml-2 rounded-xl border border-white/10 px-4 py-2 text-sm text-white hover:bg-white/10"
                >
                  ai reply
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    {aiReply && (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div className="w-full max-w-lg rounded-2xl bg-[#111111] border border-white/10 p-6">

          <h2 className="text-lg font-semibold text-white">
            ai reply for {aiReply.leadName}
          </h2>

          <p className="mt-4 text-sm text-zinc-300">
            {aiReply.text}
          </p>

          <div className="mt-6 flex justify-between items-center">
            <button
              onClick={() => {
                navigator.clipboard.writeText(aiReply.text);
              }}
              className="px-4 py-2 text-sm text-[#d4af37] border border-[#d4af37]/40 rounded-lg hover:bg-[#d4af37] hover:text-black transition"
            >
              copy
            </button>

            
            <button
              onClick={() => setAiReply(null)}
              className="px-4 py-2 text-sm text-zinc-400"
            >
              close
            </button>
            
          </div>

        </div>
      </div>
    )}

  </>
);  
}
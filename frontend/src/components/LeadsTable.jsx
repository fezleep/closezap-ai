export function LeadsTable({ leads, onCloseLead }) {
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

  return (
    <div className="overflow-hidden rounded-2xl border border-white/10">
      <table className="min-w-full divide-y divide-white/10">
        <thead className="bg-black/20">
          <tr>
            <th className="px-5 py-4 text-left text-xs font-medium uppercase tracking-wider text-zinc-500">lead</th>
            <th className="px-5 py-4 text-left text-xs font-medium uppercase tracking-wider text-zinc-500">interest</th>
            <th className="px-5 py-4 text-left text-xs font-medium uppercase tracking-wider text-zinc-500">status</th>
            <th className="px-5 py-4 text-left text-xs font-medium uppercase tracking-wider text-zinc-500">intent</th>
            <th className="px-5 py-4 text-left text-xs font-medium uppercase tracking-wider text-zinc-500">last message</th>
            <th className="px-5 py-4 text-right text-xs font-medium uppercase tracking-wider text-zinc-500">action</th>
          </tr>
        </thead>

        <tbody className="divide-y divide-white/10 bg-[#111111]">
          {leads.map((lead) => (
            <tr
              key={lead.id}
              className={`transition ${
                lead._highlight
                  ? 'bg-[#d4af37]/10'
                  : 'hover:bg-white/[0.03]'
              }`}
            >
              <td className="px-5 py-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full border border-[#d4af37]/40 bg-black text-[#d4af37] font-semibold">
                    {lead.name ? lead.name.charAt(0).toUpperCase() : '?'}
                  </div>

                  <div>
                    <p className="font-medium text-white">{lead.name || 'Unnamed lead'}</p>
                    <p className="text-sm text-zinc-500">{lead.phone}</p>
                  </div>
                </div>
              </td>

              <td className="px-5 py-5 text-sm text-zinc-300">{lead.interest || '-'}</td>
              <td className="px-5 py-5">{getStatusBadge(lead.status)}</td>
              <td className="px-5 py-5">{getIntentText(lead.intent)}</td>

              <td className="max-w-xs px-5 py-5 text-sm text-zinc-500">
                {truncateMessage(lead.lastMessage || lead.last_message)}
              </td>

              <td className="px-5 py-5 text-right">
                {lead.status !== 'closed' ? (
                  <button
                    onClick={() => handleClose(lead.id)}
                    className="rounded-xl border border-[#d4af37]/40 px-4 py-2 text-sm font-medium text-[#d4af37] hover:bg-[#d4af37] hover:text-black transition"
                  >
                    closing...
                  </button>
                ) : (
                  <span className="text-sm text-zinc-500">closed</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
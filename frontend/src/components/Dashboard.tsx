import { useEffect, useState } from "react";

/**
 * Dashboard component displays system statistics fetched from the backend.
 */
export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/logs")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Error fetching stats:", err));
  }, []);

  if (!stats) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          📊 System Statistics
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Total Chats Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">Total Chats</p>
                <p className="text-4xl font-bold text-blue-600">{stats.total_chats}</p>
              </div>
              <div className="text-5xl">💬</div>
            </div>
          </div>

          {/* Chats with Feedback Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">Chats with Feedback</p>
                <p className="text-4xl font-bold text-green-600">{stats.chats_with_feedback}</p>
              </div>
              <div className="text-5xl">✅</div>
            </div>
          </div>

          {/* Positive Feedback Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">Positive Feedback</p>
                <p className="text-4xl font-bold text-purple-600">
                  {stats.positive_feedback_percent}%
                </p>
              </div>
              <div className="text-5xl">⭐</div>
            </div>
          </div>

          {/* Average Duration Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">Average Duration</p>
                <p className="text-4xl font-bold text-orange-600">
                  {(stats.avg_conversation_duration_sec / 60).toFixed(1)} min
                </p>
              </div>
              <div className="text-5xl">⏱️</div>
            </div>
          </div>
        </div>

        {/* Summary Card */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Summary</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center border-b pb-2">
              <span className="text-gray-600">Feedback Response Rate:</span>
              <span className="font-semibold">
                {stats.total_chats > 0 
                  ? Math.round((stats.chats_with_feedback / stats.total_chats) * 100)
                  : 0}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average Chat Time:</span>
              <span className="font-semibold">
                {Math.floor(stats.avg_conversation_duration_sec / 60)}:{
                  String(Math.round(stats.avg_conversation_duration_sec % 60)).padStart(2, '0')
                } minutes
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
import { useState, useEffect } from 'react';
import { Tabs } from '../components/Tabs';
import { LeaderboardTable } from '../components/LeaderboardTable';
import { getLeaderboard } from '../api/leaderboard';
import type { LeaderboardEntry } from '../types';

const PAGE_SIZE = 20;

export function LeaderboardPage() {
  const [activeTab, setActiveTab] = useState<'weekly' | 'all-time'>('weekly');
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeaderboard();
  }, [activeTab, currentPage]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await getLeaderboard(activeTab, currentPage, PAGE_SIZE);
      setEntries(response.entries);
      setTotalCount(response.totalCount);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId as 'weekly' | 'all-time');
    setCurrentPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Leaderboard</h1>

        <div className="bg-white rounded-lg shadow-md">
          <Tabs
            tabs={[
              { id: 'weekly', label: 'Weekly' },
              { id: 'all-time', label: 'All-time' },
            ]}
            activeTab={activeTab}
            onTabChange={handleTabChange}
          />

          <div className="p-6">
            {loading ? (
              <div className="text-center py-12">
                <p className="text-gray-600">Loading leaderboard...</p>
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            ) : entries.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-600">No entries found.</p>
              </div>
            ) : (
              <>
                <LeaderboardTable entries={entries} />
                
                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="mt-6 flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                      Showing {(currentPage - 1) * PAGE_SIZE + 1} to{' '}
                      {Math.min(currentPage * PAGE_SIZE, totalCount)} of {totalCount} entries
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                        disabled={currentPage === 1}
                        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                      >
                        Previous
                      </button>
                      <button
                        onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                        disabled={currentPage === totalPages}
                        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


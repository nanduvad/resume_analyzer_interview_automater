import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import JobManager from '../components/admin/JobManager';
import AnalyticsDashboard from '../components/admin/AnalyticsDashboard';
import { WithPermission } from '../components/auth/WithPermission';
import { Permission } from '../types/rbac.types';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../lib/api';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalCandidates: 0,
    averageScore: 0,
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [jobsRes, candidatesRes] = await Promise.all([
        api.getJobs(),
        api.getCandidates(),
      ]);
      
      setStats({
        totalJobs: jobsRes.data?.jobs?.length || 0,
        totalCandidates: candidatesRes.data?.candidates?.length || 0,
        averageScore: 78, // Mock average
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">
            {/* Welcome Section */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">
                Welcome back, {user?.name || user?.email}! Here's your hiring overview.
              </p>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-blue-100 rounded-lg mr-4">
                    <span className="text-blue-600 font-bold">📋</span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Active Jobs</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.totalJobs}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-green-100 rounded-lg mr-4">
                    <span className="text-green-600 font-bold">👥</span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Total Candidates</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.totalCandidates}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-purple-100 rounded-lg mr-4">
                    <span className="text-purple-600 font-bold">🎯</span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Avg Match Score</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.averageScore}%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Role-based Features */}
            <div className="space-y-6">
              {/* Job Management (Recruiters/Admins) */}
              <WithPermission permission={Permission.VIEW_ALL_JOBS}>
                <JobManager />
              </WithPermission>

              {/* Analytics (Admins/Hiring Managers) */}
              <WithPermission permission={Permission.VIEW_ANALYTICS}>
                <AnalyticsDashboard />
              </WithPermission>

              {/* Candidate View */}
              {user?.role === 'candidate' && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Applications</h2>
                  <p className="text-gray-600">
                    You have applied to 3 positions. Check your application status below.
                  </p>
                  {/* Candidate-specific content would go here */}
                </div>
              )}

              {/* AI Configuration (Admins only) */}
              <WithPermission permission={Permission.CONFIGURE_AI}>
                <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">AI Configuration</h2>
                  <p className="text-gray-600 mb-4">
                    Configure AI models, scoring algorithms, and matching parameters.
                  </p>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Matching Threshold
                      </label>
                      <input 
                        type="range" 
                        min="0" 
                        max="100" 
                        defaultValue="70"
                        className="w-full"
                      />
                    </div>
                    <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
                      Save Configuration
                    </button>
                  </div>
                </div>
              </WithPermission>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;

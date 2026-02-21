import React from 'react';
import { Link } from 'react-router-dom';
import Header from '@components/Header';
import Footer from '@components/Footer';
import FeatureCard from '@components/FeatureCard';
import Testimonial from '@components/Testimonial';

const LandingPage: React.FC = () => {
  const features = [
    {
      title: 'AI-Powered Candidate Matching',
      description: 'Advanced algorithms to match candidates with job requirements',
      icon: '🎯'
    },
    {
      title: 'Automated Interview Questions',
      description: 'Generate tailored interview questions based on job descriptions',
      icon: '💬'
    },
    {
      title: 'Real-time Scoring',
      description: 'Instant candidate evaluation with detailed scoring breakdown',
      icon: '⚡'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'HR Director at TechCorp',
      content: 'Reduced our hiring time by 70% with accurate AI matching.',
      avatar: '👩‍💼'
    },
    {
      name: 'Mike Chen',
      role: 'Engineering Manager at StartupXYZ',
      content: 'The interview question generator is a game-changer for technical roles.',
      avatar: '👨‍💻'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <section className="py-20 px-4 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          AI-Powered Talent Matching Platform
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Streamline your hiring process with intelligent candidate matching, 
          automated interview questions, and real-time scoring.
        </p>
        <Link 
          to="/dashboard" 
          className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
        >
          Launch Dashboard
        </Link>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                title={feature.title}
                description={feature.description}
                icon={feature.icon}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-4 bg-gray-100">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {testimonials.map((testimonial, index) => (
              <Testimonial
                key={index}
                name={testimonial.name}
                role={testimonial.role}
                content={testimonial.content}
                avatar={testimonial.avatar}
              />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Hiring?</h2>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Join hundreds of companies using TalentMatch to find the perfect candidates faster.
        </p>
        <Link 
          to="/dashboard" 
          className="bg-green-600 text-white px-10 py-4 rounded-lg text-xl font-semibold hover:bg-green-700 transition"
        >
          Get Started Free
        </Link>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;

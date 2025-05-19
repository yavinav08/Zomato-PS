import { useParams, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../api';
import type { Restaurant } from '../types';

const RestaurantDetail = () => {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRestaurant = async () => {
      try {
        setLoading(true);
        const response = await api.get<Restaurant>(`/restaurants/${id}/`);
        setRestaurant(response.data);
        setError(null);
      } catch (err: any) {
        console.error('Error fetching restaurant:', err);
        setError('Failed to load restaurant details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchRestaurant();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="animate-pulse space-y-8">
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <div className="h-2 w-2 rounded-full bg-red-400"></div>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error || 'Restaurant not found'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <Link
          to="/"
          className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-500 mb-8"
        >
          <div className="w-2 h-2 mr-1 rounded-full bg-blue-600"></div>
          Back to Restaurants
        </Link>

        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="p-6 sm:p-8">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-3xl font-bold text-gray-900">{restaurant.name}</h1>
              <div className="flex items-center bg-green-500 text-white px-2.5 py-0.5 rounded-full">
                <div className="w-2 h-2 mr-1 rounded-full bg-white"></div>
                <span className="font-semibold text-sm">{restaurant.aggregate_rating}</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h2 className="text-sm font-medium text-gray-500">Location</h2>
                  <div className="mt-1 flex items-center text-gray-900">
                    <div className="w-2 h-2 mr-1 rounded-full bg-gray-400"></div>
                    {restaurant.city}
                  </div>
                </div>

                <div>
                  <h2 className="text-sm font-medium text-gray-500">Cuisines</h2>
                  <div className="mt-1 flex items-center text-gray-900">
                    <div className="w-2 h-2 mr-1 rounded-full bg-gray-400"></div>
                    {restaurant.cuisines}
                  </div>
                </div>

                <div>
                  <h2 className="text-sm font-medium text-gray-500">Address</h2>
                  <p className="mt-1 text-gray-900">{restaurant.address}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h2 className="text-sm font-medium text-gray-500">Rating Details</h2>
                  <div className="mt-1 flex items-center text-gray-900">
                    <div className="w-2 h-2 mr-1 rounded-full bg-gray-400"></div>
                    {restaurant.votes} votes
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RestaurantDetail;

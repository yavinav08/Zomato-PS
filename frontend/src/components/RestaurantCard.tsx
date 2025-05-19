import { Link } from 'react-router-dom';
import type { Restaurant } from '../types';

interface Props {
  restaurant: Restaurant;
}

const RestaurantCard = ({ restaurant }: Props) => (
  <div className="group relative bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
    {/* Rating Badge */}
    <div className="absolute top-4 right-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-3 py-1.5 rounded-full text-sm font-semibold shadow-sm">
      {restaurant.aggregate_rating} •
    </div>
    
    <div className="p-6">
      {/* Restaurant Name */}
      <h2 className="text-xl font-bold text-gray-900 mb-4 line-clamp-1 font-display">
        {restaurant.name}
      </h2>
      
      {/* Details */}
      <div className="space-y-3">
        <div className="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
          <div className="w-2 h-2 mr-2 rounded-full bg-blue-400"></div>
          <span className="text-sm font-medium">{restaurant.city}</span>
        </div>

        <div className="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
          <div className="w-2 h-2 mr-2 rounded-full bg-purple-400"></div>
          <span className="text-sm font-medium line-clamp-1">{restaurant.cuisines}</span>
        </div>

        <div className="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
          <div className="w-2 h-2 mr-2 rounded-full bg-amber-400"></div>
          <span className="text-sm font-medium">{restaurant.votes} votes</span>
        </div>
      </div>

      {/* View Details Button */}
      <Link 
        to={`/restaurant/${restaurant.id}`}
        className="mt-6 inline-flex items-center justify-center w-full px-4 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-sm font-semibold rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 shadow-sm hover:shadow-md"
      >
        View Details
        <div className="w-2 h-2 ml-2 rounded-full bg-white"></div>
      </Link>
    </div>
  </div>
);

export default RestaurantCard;

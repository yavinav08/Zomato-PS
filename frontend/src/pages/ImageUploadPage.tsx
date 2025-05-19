import ImageUpload from '../components/ImageUpload';
import { Link } from 'react-router-dom';

const ImageUploadPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <Link
            to="/"
            className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-500 mb-8"
          >
            <div className="w-2 h-2 mr-1 rounded-full bg-blue-600"></div>
            Back to Home
          </Link>
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Food Image Recognition
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Upload a food image to find matching restaurants
          </p>
        </div>

        <ImageUpload />
      </div>
    </div>
  );
};

export default ImageUploadPage; 
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { User, Edit } from 'lucide-react'

function Profile({ user, token, onUserUpdate }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600">Manage your personal information and health profile</p>
        </div>
        <Button>
          <Edit className="h-4 w-4 mr-2" />
          Edit Profile
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <User className="h-5 w-5 mr-2 text-blue-500" />
            Personal Information
          </CardTitle>
          <CardDescription>Your account and health profile details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">Username</label>
              <p className="text-gray-900">{user.username}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Email</label>
              <p className="text-gray-900">{user.email}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Age</label>
              <p className="text-gray-900">{user.age || 'Not specified'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Gender</label>
              <p className="text-gray-900">{user.gender || 'Not specified'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Height</label>
              <p className="text-gray-900">{user.height ? `${user.height} cm` : 'Not specified'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Weight</label>
              <p className="text-gray-900">{user.weight ? `${user.weight} kg` : 'Not specified'}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Profile


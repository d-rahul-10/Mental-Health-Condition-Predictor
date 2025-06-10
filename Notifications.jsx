import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Bell, Plus } from 'lucide-react'

function Notifications({ user, token }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
          <p className="text-gray-600">Manage your health reminders and alerts</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Reminder
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bell className="h-5 w-5 mr-2 text-yellow-500" />
            Recent Notifications
          </CardTitle>
          <CardDescription>Your latest health reminders and alerts</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-center text-gray-500 py-8">
            No notifications yet. Set up reminders to stay on track!
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default Notifications


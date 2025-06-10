import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Target, Plus } from 'lucide-react'

function Goals({ user, token }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Health Goals</h1>
          <p className="text-gray-600">Set and track your health objectives</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add New Goal
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2 text-blue-500" />
            Your Goals
          </CardTitle>
          <CardDescription>Track your progress towards better health</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-center text-gray-500 py-8">
            No goals set yet. Create your first goal to get started!
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default Goals


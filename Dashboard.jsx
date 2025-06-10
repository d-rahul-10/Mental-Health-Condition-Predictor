import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Heart, Activity, Target, TrendingUp, Calendar, Plus } from 'lucide-react'

function Dashboard({ user, token }) {
  const [healthSummary, setHealthSummary] = useState(null)
  const [goals, setGoals] = useState([])
  const [recentRecords, setRecentRecords] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch health summary
      const summaryResponse = await fetch('http://localhost:5000/api/health/summary', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json()
        setHealthSummary(summaryData)
      }

      // Fetch active goals
      const goalsResponse = await fetch('http://localhost:5000/api/goals?status=active', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (goalsResponse.ok) {
        const goalsData = await goalsResponse.json()
        setGoals(goalsData.slice(0, 3)) // Show only first 3 goals
      }

      // Fetch recent health records
      const recordsResponse = await fetch('http://localhost:5000/api/health/records?limit=5', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (recordsResponse.ok) {
        const recordsData = await recordsResponse.json()
        setRecentRecords(recordsData)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const calculateBMI = () => {
    if (user.height && user.weight) {
      const heightInM = user.height / 100
      return (user.weight / (heightInM * heightInM)).toFixed(1)
    }
    return null
  }

  const getBMICategory = (bmi) => {
    if (bmi < 18.5) return { category: 'Underweight', color: 'text-blue-600' }
    if (bmi < 25) return { category: 'Normal', color: 'text-green-600' }
    if (bmi < 30) return { category: 'Overweight', color: 'text-yellow-600' }
    return { category: 'Obese', color: 'text-red-600' }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const bmi = calculateBMI()
  const bmiInfo = bmi ? getBMICategory(parseFloat(bmi)) : null

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome back, {user.username}!</h1>
        <p className="text-blue-100">
          Here's your health overview for today. Keep up the great work!
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">BMI</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {bmi || 'N/A'}
            </div>
            {bmiInfo && (
              <p className={`text-xs ${bmiInfo.color}`}>
                {bmiInfo.category}
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Goals</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{goals.length}</div>
            <p className="text-xs text-muted-foreground">
              Goals in progress
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Records This Week</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {healthSummary ? Object.values(healthSummary.health_records_summary).reduce((sum, record) => sum + record.count_last_7_days, 0) : 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Health entries logged
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Health Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85%</div>
            <p className="text-xs text-muted-foreground">
              Overall health rating
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Goals Progress */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Active Goals
              <Button size="sm" onClick={() => window.location.href = '/goals'}>
                <Plus className="h-4 w-4 mr-1" />
                Add Goal
              </Button>
            </CardTitle>
            <CardDescription>
              Track your progress towards your health goals
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {goals.length > 0 ? (
              goals.map((goal) => (
                <div key={goal.id} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{goal.title}</span>
                    <span className="text-muted-foreground">
                      {goal.progress_percentage.toFixed(0)}%
                    </span>
                  </div>
                  <Progress value={goal.progress_percentage} className="h-2" />
                  <p className="text-xs text-muted-foreground">
                    {goal.current_value} / {goal.target_value} {goal.unit}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-muted-foreground text-center py-4">
                No active goals. Create your first goal to get started!
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Recent Activity
              <Button size="sm" variant="outline" onClick={() => window.location.href = '/tracking'}>
                View All
              </Button>
            </CardTitle>
            <CardDescription>
              Your latest health records and activities
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentRecords.length > 0 ? (
              recentRecords.map((record) => (
                <div key={record.id} className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium capitalize">
                      {record.record_type.replace('_', ' ')}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(record.recorded_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {typeof record.value === 'object' ? 
                      Object.values(record.value)[0] : 
                      record.value
                    }
                  </div>
                </div>
              ))
            ) : (
              <p className="text-muted-foreground text-center py-4">
                No recent activity. Start tracking your health data!
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>
            Common tasks to help you stay on top of your health
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button 
              variant="outline" 
              className="h-20 flex flex-col items-center justify-center space-y-2"
              onClick={() => window.location.href = '/tracking'}
            >
              <Heart className="h-6 w-6" />
              <span className="text-sm">Log Health Data</span>
            </Button>
            
            <Button 
              variant="outline" 
              className="h-20 flex flex-col items-center justify-center space-y-2"
              onClick={() => window.location.href = '/goals'}
            >
              <Target className="h-6 w-6" />
              <span className="text-sm">Set New Goal</span>
            </Button>
            
            <Button 
              variant="outline" 
              className="h-20 flex flex-col items-center justify-center space-y-2"
              onClick={() => window.location.href = '/notifications'}
            >
              <Calendar className="h-6 w-6" />
              <span className="text-sm">Set Reminder</span>
            </Button>
            
            <Button 
              variant="outline" 
              className="h-20 flex flex-col items-center justify-center space-y-2"
              onClick={() => window.location.href = '/profile'}
            >
              <Activity className="h-6 w-6" />
              <span className="text-sm">Update Profile</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard


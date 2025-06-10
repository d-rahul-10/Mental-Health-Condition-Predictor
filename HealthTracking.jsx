import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Heart, Activity, Utensils, Pill, Brain, Droplets } from 'lucide-react'

function HealthTracking({ user, token }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Health Tracking</h1>
          <p className="text-gray-600">Log and monitor your health data</p>
        </div>
      </div>

      <Tabs defaultValue="vitals" className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="vitals">Vitals</TabsTrigger>
          <TabsTrigger value="exercise">Exercise</TabsTrigger>
          <TabsTrigger value="nutrition">Nutrition</TabsTrigger>
          <TabsTrigger value="medication">Medication</TabsTrigger>
          <TabsTrigger value="symptoms">Symptoms</TabsTrigger>
          <TabsTrigger value="sleep">Sleep</TabsTrigger>
        </TabsList>

        <TabsContent value="vitals" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Heart className="h-5 w-5 mr-2 text-red-500" />
                  Blood Pressure
                </CardTitle>
                <CardDescription>Record your blood pressure readings</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full">Log Blood Pressure</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-blue-500" />
                  Heart Rate
                </CardTitle>
                <CardDescription>Track your heart rate measurements</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full">Log Heart Rate</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="exercise" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="h-5 w-5 mr-2 text-green-500" />
                Exercise & Activity
              </CardTitle>
              <CardDescription>Log your workouts and physical activities</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">Log Exercise</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="nutrition" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Utensils className="h-5 w-5 mr-2 text-orange-500" />
                Nutrition & Diet
              </CardTitle>
              <CardDescription>Track your meals and nutritional intake</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">Log Meal</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="medication" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Pill className="h-5 w-5 mr-2 text-purple-500" />
                Medication
              </CardTitle>
              <CardDescription>Track your medication intake and schedules</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">Log Medication</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="symptoms" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Brain className="h-5 w-5 mr-2 text-pink-500" />
                Symptoms & Mood
              </CardTitle>
              <CardDescription>Record symptoms and track your mood</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">Log Symptoms</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sleep" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Droplets className="h-5 w-5 mr-2 text-indigo-500" />
                Sleep & Hydration
              </CardTitle>
              <CardDescription>Track your sleep patterns and water intake</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">Log Sleep</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default HealthTracking


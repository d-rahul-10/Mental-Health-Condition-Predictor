from flask import Blueprint, jsonify, request
from src.models.user import Goal, db
from src.routes.auth import token_required
from datetime import datetime
import json

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('', methods=['GET'])
@token_required
def get_goals(current_user):
    try:
        status = request.args.get('status')  # active, completed, paused, cancelled
        goal_type = request.args.get('type')
        
        query = Goal.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        if goal_type:
            query = query.filter_by(goal_type=goal_type)
        
        goals = query.order_by(Goal.created_at.desc()).all()
        
        return jsonify([goal.to_dict() for goal in goals]), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch goals: {str(e)}'}), 500

@goals_bp.route('', methods=['POST'])
@token_required
def create_goal(current_user):
    try:
        data = request.json
        
        if not data.get('goal_type') or not data.get('title'):
            return jsonify({'message': 'Goal type and title are required'}), 400
        
        # Validate goal type
        valid_types = ['weight_loss', 'weight_gain', 'exercise', 'medication_adherence', 'blood_pressure', 'heart_rate', 'sleep', 'water_intake', 'diet', 'custom']
        if data['goal_type'] not in valid_types:
            return jsonify({'message': f'Invalid goal type. Must be one of: {", ".join(valid_types)}'}), 400
        
        goal = Goal(
            user_id=current_user.id,
            goal_type=data['goal_type'],
            title=data['title'],
            description=data.get('description'),
            target_value=data.get('target_value'),
            current_value=data.get('current_value', 0),
            unit=data.get('unit'),
            deadline=datetime.fromisoformat(data['deadline'].replace('Z', '+00:00')) if data.get('deadline') else None,
            status=data.get('status', 'active')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'message': 'Goal created successfully',
            'goal': goal.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create goal: {str(e)}'}), 500

@goals_bp.route('/<int:goal_id>', methods=['GET'])
@token_required
def get_goal(current_user, goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
        
        return jsonify(goal.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch goal: {str(e)}'}), 500

@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@token_required
def update_goal(current_user, goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
        
        data = request.json
        
        if 'title' in data:
            goal.title = data['title']
        if 'description' in data:
            goal.description = data['description']
        if 'target_value' in data:
            goal.target_value = data['target_value']
        if 'current_value' in data:
            goal.current_value = data['current_value']
        if 'unit' in data:
            goal.unit = data['unit']
        if 'deadline' in data:
            goal.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00')) if data['deadline'] else None
        if 'status' in data:
            goal.status = data['status']
        
        goal.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to update goal: {str(e)}'}), 500

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@token_required
def delete_goal(current_user, goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({'message': 'Goal deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to delete goal: {str(e)}'}), 500

@goals_bp.route('/<int:goal_id>/progress', methods=['POST'])
@token_required
def update_goal_progress(current_user, goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
        
        data = request.json
        
        if 'current_value' not in data:
            return jsonify({'message': 'Current value is required'}), 400
        
        goal.current_value = data['current_value']
        goal.updated_at = datetime.utcnow()
        
        # Check if goal is completed
        if goal.target_value and goal.current_value >= goal.target_value:
            goal.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Goal progress updated successfully',
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to update goal progress: {str(e)}'}), 500

@goals_bp.route('/suggestions', methods=['GET'])
@token_required
def get_goal_suggestions(current_user):
    try:
        suggestions = []
        
        # Weight management suggestions
        if current_user.weight and current_user.height:
            height_m = current_user.height / 100
            bmi = current_user.weight / (height_m ** 2)
            
            if bmi > 25:
                suggestions.append({
                    'goal_type': 'weight_loss',
                    'title': 'Lose Weight to Healthy BMI',
                    'description': f'Your current BMI is {bmi:.1f}. Consider losing weight to reach a healthy BMI range (18.5-24.9).',
                    'target_value': round(24.9 * (height_m ** 2), 1),
                    'unit': 'kg',
                    'priority': 'high'
                })
            elif bmi < 18.5:
                suggestions.append({
                    'goal_type': 'weight_gain',
                    'title': 'Gain Weight to Healthy BMI',
                    'description': f'Your current BMI is {bmi:.1f}. Consider gaining weight to reach a healthy BMI range (18.5-24.9).',
                    'target_value': round(18.5 * (height_m ** 2), 1),
                    'unit': 'kg',
                    'priority': 'high'
                })
        
        # Exercise suggestions based on activity level
        if current_user.activity_level in ['sedentary', 'light']:
            suggestions.append({
                'goal_type': 'exercise',
                'title': 'Increase Daily Exercise',
                'description': 'Aim for at least 150 minutes of moderate-intensity exercise per week.',
                'target_value': 150,
                'unit': 'minutes/week',
                'priority': 'medium'
            })
        
        # Water intake suggestion
        suggestions.append({
            'goal_type': 'water_intake',
            'title': 'Daily Water Intake',
            'description': 'Drink at least 8 glasses of water per day for optimal hydration.',
            'target_value': 8,
            'unit': 'glasses/day',
            'priority': 'medium'
        })
        
        # Sleep suggestion
        suggestions.append({
            'goal_type': 'sleep',
            'title': 'Healthy Sleep Schedule',
            'description': 'Aim for 7-9 hours of quality sleep each night.',
            'target_value': 8,
            'unit': 'hours/night',
            'priority': 'medium'
        })
        
        return jsonify({
            'suggestions': suggestions,
            'message': f'Generated {len(suggestions)} personalized goal suggestions'
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to generate goal suggestions: {str(e)}'}), 500


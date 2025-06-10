from flask import Blueprint, jsonify, request
from src.models.user import HealthRecord, db
from src.routes.auth import token_required
from datetime import datetime, timedelta
import json

health_bp = Blueprint('health', __name__)

@health_bp.route('/records', methods=['GET'])
@token_required
def get_health_records(current_user):
    try:
        # Get query parameters
        record_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = HealthRecord.query.filter_by(user_id=current_user.id)
        
        if record_type:
            query = query.filter_by(record_type=record_type)
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(HealthRecord.recorded_at >= start_date)
        
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(HealthRecord.recorded_at <= end_date)
        
        records = query.order_by(HealthRecord.recorded_at.desc()).limit(limit).all()
        
        return jsonify([record.to_dict() for record in records]), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch health records: {str(e)}'}), 500

@health_bp.route('/records', methods=['POST'])
@token_required
def create_health_record(current_user):
    try:
        data = request.json
        
        if not data.get('record_type') or not data.get('value'):
            return jsonify({'message': 'Record type and value are required'}), 400
        
        # Validate record type
        valid_types = ['blood_pressure', 'heart_rate', 'weight', 'exercise', 'diet', 'medication', 'symptoms', 'sleep', 'water_intake']
        if data['record_type'] not in valid_types:
            return jsonify({'message': f'Invalid record type. Must be one of: {", ".join(valid_types)}'}), 400
        
        record = HealthRecord(
            user_id=current_user.id,
            record_type=data['record_type'],
            value=json.dumps(data['value']),
            notes=data.get('notes'),
            recorded_at=datetime.fromisoformat(data['recorded_at'].replace('Z', '+00:00')) if data.get('recorded_at') else datetime.utcnow()
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Health record created successfully',
            'record': record.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create health record: {str(e)}'}), 500

@health_bp.route('/records/<int:record_id>', methods=['GET'])
@token_required
def get_health_record(current_user, record_id):
    try:
        record = HealthRecord.query.filter_by(id=record_id, user_id=current_user.id).first()
        
        if not record:
            return jsonify({'message': 'Health record not found'}), 404
        
        return jsonify(record.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch health record: {str(e)}'}), 500

@health_bp.route('/records/<int:record_id>', methods=['PUT'])
@token_required
def update_health_record(current_user, record_id):
    try:
        record = HealthRecord.query.filter_by(id=record_id, user_id=current_user.id).first()
        
        if not record:
            return jsonify({'message': 'Health record not found'}), 404
        
        data = request.json
        
        if 'value' in data:
            record.value = json.dumps(data['value'])
        if 'notes' in data:
            record.notes = data['notes']
        if 'recorded_at' in data:
            record.recorded_at = datetime.fromisoformat(data['recorded_at'].replace('Z', '+00:00'))
        
        db.session.commit()
        
        return jsonify({
            'message': 'Health record updated successfully',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to update health record: {str(e)}'}), 500

@health_bp.route('/records/<int:record_id>', methods=['DELETE'])
@token_required
def delete_health_record(current_user, record_id):
    try:
        record = HealthRecord.query.filter_by(id=record_id, user_id=current_user.id).first()
        
        if not record:
            return jsonify({'message': 'Health record not found'}), 404
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message': 'Health record deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to delete health record: {str(e)}'}), 500

@health_bp.route('/summary', methods=['GET'])
@token_required
def get_health_summary(current_user):
    try:
        # Get recent records for each type
        summary = {}
        record_types = ['blood_pressure', 'heart_rate', 'weight', 'exercise', 'diet', 'medication', 'symptoms', 'sleep', 'water_intake']
        
        for record_type in record_types:
            latest_record = HealthRecord.query.filter_by(
                user_id=current_user.id,
                record_type=record_type
            ).order_by(HealthRecord.recorded_at.desc()).first()
            
            if latest_record:
                summary[record_type] = {
                    'latest': latest_record.to_dict(),
                    'count_last_7_days': HealthRecord.query.filter_by(
                        user_id=current_user.id,
                        record_type=record_type
                    ).filter(
                        HealthRecord.recorded_at >= datetime.utcnow() - timedelta(days=7)
                    ).count()
                }
            else:
                summary[record_type] = {
                    'latest': None,
                    'count_last_7_days': 0
                }
        
        # Calculate BMI if height and weight are available
        bmi = None
        if current_user.height and current_user.weight:
            height_m = current_user.height / 100  # convert cm to m
            bmi = round(current_user.weight / (height_m ** 2), 1)
        
        return jsonify({
            'user_profile': current_user.to_dict_safe(),
            'bmi': bmi,
            'health_records_summary': summary,
            'total_records': HealthRecord.query.filter_by(user_id=current_user.id).count()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to generate health summary: {str(e)}'}), 500

@health_bp.route('/analytics/trends', methods=['GET'])
@token_required
def get_health_trends(current_user):
    try:
        record_type = request.args.get('type', 'weight')
        days = request.args.get('days', 30, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        records = HealthRecord.query.filter_by(
            user_id=current_user.id,
            record_type=record_type
        ).filter(
            HealthRecord.recorded_at >= start_date
        ).order_by(HealthRecord.recorded_at.asc()).all()
        
        trends = []
        for record in records:
            value_data = json.loads(record.value)
            trends.append({
                'date': record.recorded_at.isoformat(),
                'value': value_data,
                'notes': record.notes
            })
        
        return jsonify({
            'record_type': record_type,
            'period_days': days,
            'trends': trends
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to generate trends: {str(e)}'}), 500


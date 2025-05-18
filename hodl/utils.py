# utils.py
import json
import logging

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        elif hasattr(obj, 'data'):
            return obj.data
        try:
            return obj.__dict__
        except AttributeError:
            return str(obj)

def log_order_response(order, logger, operation_type="Order"):
    """Helper function to log order responses in a consistent way"""
    try:
        logger.info(f"{operation_type} placed: {json.dumps(order, indent=2, cls=CustomJSONEncoder)}")
    except Exception as e:
        logger.error(f"Error serializing order: {e}")
        logger.info(f"{operation_type} placed (not serialized): {str(order)}")

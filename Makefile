inventory:
			uvicorn inventory-service.main:app --reload

payment:
			uvicorn payment-service.main:app --reload
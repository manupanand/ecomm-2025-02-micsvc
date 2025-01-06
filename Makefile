inventory:
			uvicorn inventory-service.main:app --reload --port 3500

payment:
		 uvicorn payment-service.main:app --reload --port 2500


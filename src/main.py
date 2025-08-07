"""Entrypoint for the application."""

import asyncio

from routes.costumer_routes import CostumerERPRoute
from payload_translator.payload_translator import PayloadTranslator
from services.tracos_service import TracOsService

async def process_workorder(order_no: int, costumer_route, payload_translator, tracos_service):
    """Process a single workorder through the complete pipeline."""
    
    print(f"\n--- Processing workorder {order_no} ---")
    

    costumer_workorder = await costumer_route.get_costumer_workorder_by_order_number(order_no)
    if not costumer_workorder:
        print(f"Workorder {order_no} not found in customer system.")
        return False


    tracos_payload = payload_translator.from_costumer_to_tracos(payload=costumer_workorder)
    if not tracos_payload:
        print(f"Failed to translate customer workorder {order_no} to Tracos format.")
        return False

    inserted_workorder = await tracos_service.insert_workorder(tracos_payload)
    if not inserted_workorder:
        print(f"Failed to insert workorder {order_no} into Tracos (MongoDB).")
        return False


    queried_workorder = await tracos_service.get_workorder_by_number(order_no)
    if not queried_workorder:
        print(f"Workorder {order_no} not found in Tracos (MongoDB).")
        return False


    translated_costumer_workorder = payload_translator.from_tracos_to_costumer(payload=queried_workorder)

    result = await costumer_route.post_costumer_workorder(translated_costumer_workorder)
    if result:
        print(f"Workorder {order_no} processed and recorded in outbound folder.")
        return True
    else:
        print(f"Failed to record workorder {order_no} in outbound folder.")
        return False

async def main():

    costumer_route = CostumerERPRoute()
    payload_translator = PayloadTranslator()
    tracos_service = TracOsService()


    workorder_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print(f"Starting to process {len(workorder_numbers)} workorders...")
 
    successful_count = 0
    failed_count = 0
    
    for order_no in workorder_numbers:
        try:
            success = await process_workorder(order_no, costumer_route, payload_translator, tracos_service)
            if success:
                successful_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"Error processing workorder {order_no}: {str(e)}")
            failed_count += 1

    print(f"\n--- Processing Complete ---")
    print(f"Successfully processed: {successful_count} workorders")
    print(f"Failed to process: {failed_count} workorders")
    print(f"Total workorders: {len(workorder_numbers)}")


if __name__ == "__main__":
    asyncio.run(main())

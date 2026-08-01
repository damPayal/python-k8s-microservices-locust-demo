from locust import HttpUser, task, between,events
import random

THRESHOLDS={
    "response_time_p95":500, #ma
    "failure_rate":1.0,         #percent
}

class ShopperUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def browse_products(self):
        self.client.get("/catalog/products")

    @task(1)
    def view_product(self):
        product_id = random.choice([1, 2, 3])
        self.client.get(f"/catalog/products/{product_id}")

    @task(1)
    def place_order(self):
        items = [{"product_id": random.choice([1, 2, 3]), "quantity": random.randint(1, 3)}]
        self.client.post("/orders", json=items)

    @events.quitting.add_listener
    def check_thresholds(environment,**kwargs):
        stats=environment.stats.total
        if stats.num_requests==0:
            print("ERROR: No requests were made")
            environment.process_exit_code=1
            return

        failure_rate=(stats.num_failure/stats.num_requests)*100
        p95=stats.get_response_time_percentile(0.95)

        failures=[]

        if p95>THRESHOLDS["response_time_p95"]:
                failures.append(f"p95 too high:{p95} ms")
        if failure_rate>THRESHOLDS["failure_rate"]:
             failures.append(f"failure rate too high: {failure_rate}%")

        if failures:
            print("PERFORMANCE THRESHOLDS NOT MET:")
            for f in failures:
                  print("  -",f)
            environment.process_exit_code=1
        else:
             print("Performance thresholds met.")
             environment.process_exit_code=0    

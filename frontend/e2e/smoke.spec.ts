import { test, expect } from "@playwright/test";

test("staff console opens the patient demo", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("ClinicFlow")).toBeVisible();
  await page.getByRole("button", { name: "Patient demo" }).click();
  await expect(page.getByText("Tell us when you need your appointment")).toBeVisible();
  await expect(page.getByText("AI output is advisory until deterministic validation and human approval.")).toBeVisible();
});

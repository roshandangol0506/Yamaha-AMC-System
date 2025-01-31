document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();

  document.querySelectorAll(".customer-row").forEach(function (row) {
    // Get the no_of_service and effective_to values
    const noOfService = parseInt(row.getAttribute("data-no-of-service"));
    const effectiveToStr = row
      .querySelector("td:nth-child(11)")
      .textContent.trim(); // Effective to date is in the 10th <td>
    const effectiveToDate = new Date(effectiveToStr);

    let daysLeft = null;

    // Calculate days left if effectiveToDate is valid
    if (!isNaN(effectiveToDate)) {
      const diffTime = effectiveToDate - today;
      daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // Convert milliseconds to days
    }

    // Apply styles based on conditions
    if (noOfService === 0 || (daysLeft !== null && daysLeft <= 0)) {
      row.classList.add("expired-row"); // Add red background
    }

    // Add days left column dynamically (if required)
    const daysLeftCell = row.querySelector(".days-left");
    if (daysLeftCell) {
      if (daysLeft !== null && daysLeft > 0) {
        daysLeftCell.textContent = `${daysLeft} days left`;
      } else if (daysLeft !== null && daysLeft <= 0) {
        daysLeftCell.textContent = "Expired";
      } else {
        daysLeftCell.textContent = "No effective date";
      }
    }
  });
});

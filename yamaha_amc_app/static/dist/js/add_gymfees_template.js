document.addEventListener("DOMContentLoaded", function () {
  // Automatically set session_start_date to today's date and session_end_date to one year from today
  const sessionStartDateInput = document.getElementById("session_start_date");
  const sessionEndDateInput = document.getElementById("session_end_date");

  const today = new Date();
  const formattedToday = today.toISOString().split("T")[0]; // Format today's date as YYYY-MM-DD
  sessionStartDateInput.value = formattedToday;

  // Calculate one year from today's date
  const oneYearFromToday = new Date(today);
  oneYearFromToday.setFullYear(oneYearFromToday.getFullYear() + 1);
  const formattedOneYearFromToday = oneYearFromToday
    .toISOString()
    .split("T")[0];
  sessionEndDateInput.value = formattedOneYearFromToday;

  // Update session_end_date if session_start_date changes
  sessionStartDateInput.addEventListener("change", function () {
    const startDate = new Date(sessionStartDateInput.value);
    if (startDate) {
      const oneYearFromStartDate = new Date(startDate);
      oneYearFromStartDate.setFullYear(oneYearFromStartDate.getFullYear() + 1);
      const formattedOneYearFromStartDate = oneYearFromStartDate
        .toISOString()
        .split("T")[0];
      sessionEndDateInput.value = formattedOneYearFromStartDate;
    }
  });
});

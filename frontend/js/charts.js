let newChart = null;
let newStudentChart = null;
let newResourceChart = null;

const backgroundColor = [
	"rgba(142, 124, 195, 0.7)",
	"rgba(75, 192, 192, 0.7)",
	"rgba(255, 205, 86, 0.7)",
	"rgba(201, 203, 207, 0.7)",
	"rgba(54, 162, 235, 0.7)",
];

const borderColor = [
	"rgba(142, 124, 195, 1)",
	"rgba(75, 192, 192, 1)",
	"rgba(255, 205, 86, 1)",
	"rgba(201, 203, 207, 1)",
	"rgba(54, 162, 235, 1)",
];

// fetch data from APIs
async function getData(url) {
	try {
		const response = await fetch(url);

		if (response.ok) {
			return response.json();
		}
	} catch (e) {
		return;
	}
}

//
// Summary Charts
// ---------------
function showSummaryChart(
	elementId,
	chartTitle,
	progressValue,
	colors,
	totalValue = 100,
	suffix = "%"
) {
	const ctx = document.getElementById(elementId).getContext("2d");

	const doughnutLabel = {
		id: "doughnutLabel",
		beforeDatasetsDraw(chart, args, pluginOptions) {
			const { ctx, data } = chart;

			ctx.save();
			const xCoor = chart.getDatasetMeta(0).data[0].x;
			const yCoor = chart.getDatasetMeta(0).data[0].y;
			ctx.font = "bold 30px sans-serif";
			ctx.fillStyle = colors.textColor;
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";
			ctx.fillText(`${data.datasets[0].data[0]}${suffix}`, xCoor, yCoor);
		},
	};

	const summaryChart = new Chart(ctx, {
		type: "doughnut",
		data: {
			datasets: [
				{
					data: [progressValue, totalValue - progressValue],
					backgroundColor: [
						colors.bgColor, // Progress color
						"rgba(200, 200, 200, 0.7)", // Transparent color for remaining
					],
					borderColor: [
						colors.lineColor, // Progress color
						"rgba(200, 200, 200, 1)", // Transparent color for remaining
					],
					borderWidth: 1,
				},
			],
		},
		plugins: [doughnutLabel],
		options: {
			cutout: "80%",
			rotation: 90,
			animation: { duration: 2000 },
			plugins: {
				legend: {
					display: false,
				},
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
			},
			maintainAspectRatio: false,
		},
	});
}

// Average Teachers Activities
async function showAverageTeacherActivityScoresChart() {
	const response_data = await getData("/api/summary");

	const averageTeacherActivityScores =
		response_data.teachers.average_teacher_activity_scores;

	showSummaryChart(
		"averageTeacherActivityScoresChart",
		"Average Teacher Activity Scores",
		averageTeacherActivityScores,
		{
			bgColor: "rgba(142, 124, 195, 0.7)",
			lineColor: "rgba(142, 124, 195, 1)",
			textColor: "rgb(142, 124, 195)",
		}
	);
}
async function showAverageStudentRatingsChart() {
	const response_data = await getData("/api/summary");

	const averageStudentRatings =
		response_data.teachers.average_student_interation_ratings;

	showSummaryChart(
		"averageStudentRatingsChart",
		"Average Student Interaction Ratings",
		averageStudentRatings,
		{
			bgColor: "rgba(0, 124, 195, 0.7)",
			lineColor: "rgba(0, 124, 195, 1)",
			textColor: "rgb(0, 124, 195)",
		},
		5,
		""
	);
}

showAverageTeacherActivityScoresChart();
showAverageStudentRatingsChart();

// Average Student Progress
async function showAverageStudentAvgScoresImprovementChart() {
	const response_data = await getData("/api/summary");

	const averageStudentAvgScoresImprovement =
		response_data.students.average_student_avg_scores_improvement;

	showSummaryChart(
		"averageStudentAvgScoresImprovementChart",
		"Average Scores Improvement",
		averageStudentAvgScoresImprovement,
		{
			bgColor: "rgba(142, 124, 195, 0.7)",
			lineColor: "rgba(142, 124, 195, 1)",
			textColor: "rgb(142, 124, 195)",
		},
		15,
		"%"
	);
}

async function showAverageHomeworkCompletionRatesChart() {
	const response_data = await getData("/api/summary");

	const averageHomeworkCompletionRates =
		response_data.students.average_homework_comletion_rates;

	showSummaryChart(
		"averageHomeworkCompletionRatesChart",
		"Average Homework Completion Rates",
		averageHomeworkCompletionRates,
		{
			bgColor: "rgba(75, 192, 192, 0.7)",
			lineColor: "rgba(75, 192, 192, 1)",
			textColor: "rgb(75, 192, 192)",
		}
	);
}

async function showAverageAttendanceRatesChart() {
	const response_data = await getData("/api/summary");

	const averageAttendanceRates =
		response_data.students.average_attendace_rates;

	showSummaryChart(
		"averageAttendanceRatesChart",
		"Average Attendance Rates",
		averageAttendanceRates,
		{
			bgColor: "rgba(255, 205, 86, 0.7)",
			lineColor: "rgba(255, 205, 86, 1)",
			textColor: "rgb(255, 205, 86)",
		}
	);
}

showAverageStudentAvgScoresImprovementChart();
showAverageHomeworkCompletionRatesChart();
showAverageAttendanceRatesChart();

//
//
// Teacher Acticities Charts
// -------------------------
function showChart(
	elementId,
	chartType,
	chartTitle,
	xlabels,
	yData,
	isLegend = true,
	isShared = false,
	ySuffix = ""
) {
	const chart = document.getElementById(elementId);
	if (isShared && newChart !== null) {
		newChart.destroy();
	}
	const myChart = new Chart(chart, {
		type: chartType,
		data: {
			labels: xlabels,
			datasets: [
				{
					data: yData,
					backgroundColor,
					borderColor,
					borderWidth: 1,
				},
			],
		},

		options: {
			plugins: {
				legend: {
					display: isLegend,
				},
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
				datalabels: {
					anchor: "end",
					formatter: (value, ctx) => {
						return value + ySuffix;
					},
				},
			},
			responsive: true,
			scales: {
				y: {
					title: {
						display: true,
						text:
							chartTitle.split("by")[0] +
							`${ySuffix ? ` (${ySuffix})` : ""}`,
					},
					beginAtZero: false,
					ticks: {
						callback: function (value) {
							return value + ySuffix;
						},
					},
				},
			},
		},
		plugins: [ChartDataLabels],
	});

	if (isShared) {
		newChart = myChart;
	}
}

async function showTeacherActivityScoreChart() {
	const response_data = await getData("/api/teacher-activities");

	const teacherNames = response_data.map((item) => item.name);
	const activityScores = response_data.map((item) => item.activity_score);

	showChart(
		"teacherActivityChart",
		"bar",
		"Teacher Activity Scores by Teacher",
		teacherNames,
		activityScores,
		false,
		true,
		"%"
	);
}

async function showTeacherStudentInteractionRatingChart() {
	const response_data = await getData("/api/teacher-activities");

	const teacherNames = response_data.map((item) => item.name);
	const studentInterationRatings = response_data.map(
		(item) => item.student_interaction_rating
	);

	showChart(
		"teacherActivityChart",
		"bar",
		"Student Interaction Ratings by Teacher",
		teacherNames,
		studentInterationRatings,
		false,
		true
	);
}

function showTeacherActivityChart(value) {
	if (value === "teacherActivityScoreChart") {
		showTeacherActivityScoreChart();
	} else if (value === "studentInterationRatingChart") {
		showTeacherStudentInteractionRatingChart();
	}
}

showTeacherActivityChart("teacherActivityScoreChart");

function showSubjectsTaughtChart(
	elementId,
	chartType,
	chartTitle,
	xlabels,
	yData
) {
	const chart = document.getElementById(elementId);

	new Chart(chart, {
		type: chartType,
		data: {
			labels: xlabels,
			datasets: [
				{
					data: yData,
					backgroundColor,
					borderColor,
					borderWidth: 1,
				},
			],
		},

		options: {
			plugins: {
				legend: {
					display: true,
				},
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
				datalabels: {
					formatter: (value, ctx) => {
						return value;
					},
				},
			},
		},
		plugins: [ChartDataLabels],
	});
}

async function showTeacherSubjectsTaughtChart() {
	const response_data = await getData("/api/teacher-activities");

	const teacherNames = response_data.map((item) => item.name);
	const subjectsTaught = response_data.map(
		(item) => item.subjects_taught.length
	);

	showSubjectsTaughtChart(
		"subjectsTaughtChart",
		"doughnut",
		"Number of Subjects Taught by Teacher",
		teacherNames,
		subjectsTaught
	);
}

showTeacherSubjectsTaughtChart();

//
//
// Student Progress Charts
// -----------------------

async function showAllClassProgressRateChart(chartTitle, progressRate) {
	const response_data = await getData("/api/student-progress");

	const classIds = Array.from(
		new Set(response_data.map((item) => item.class_id))
	);

	const chart = document.getElementById("studentProgressChart");

	if (newStudentChart !== null) {
		newStudentChart.destroy();
	}

	const subjectRates = classIds.map((classId) => {
		const rates = {};
		for (const data of response_data) {
			if (!rates[data.subject]) {
				rates[data.subject] = 0;
			}

			if (data.class_id === classId) {
				rates[data.subject] = data[progressRate];
			}
		}
		return rates;
	});
	const datasets = [];
	const subjectKeys = Object.keys(subjectRates[0]);
	for (const subjectKey of subjectKeys) {
		const dataset = {
			label: subjectKey,
			data: [],
		};
		for (const rate of subjectRates) {
			if (rate[subjectKey]) {
				dataset.data.push(rate[subjectKey]);
			} else {
				dataset.data.push(0);
			}
		}
		datasets.push(dataset);
	}

	newStudentChart = new Chart(chart, {
		type: "bar",
		data: {
			labels: classIds,
			datasets,
		},
		options: {
			plugins: {
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
				datalabels: {
					anchor: "center",
					formatter: (value, ctx) => {
						return value + "%";
					},
				},
			},
			responsive: true,
			scales: {
				y: {
					title: {
						display: true,
						text: chartTitle.split("by")[0] + " (%)",
					},
					beginAtZero: false,
					ticks: {
						callback: function (value) {
							return value + "%";
						},
					},
				},
				x: {
					title: {
						display: true,
						text: "Class",
					},
				},
			},
		},
		plugins: [ChartDataLabels],
	});
}

function showStudentProgressChart(value) {
	if (value === "allClassAverageScoreImprovementChart") {
		showAllClassProgressRateChart(
			"Average Scores Improvement by Class",
			"average_score_improvement"
		);
	} else if (value === "allClassHomeworkCompletionRateChart") {
		showAllClassProgressRateChart(
			"Homework Completion Rates by Class",
			"homework_completion_rate"
		);
	} else if (value === "allClassAttendanceRateChart") {
		showAllClassProgressRateChart(
			"Attendance Rates by Class",
			"attendance_rate"
		);
	}
}

showStudentProgressChart("allClassAverageScoreImprovementChart");

//
//
// Resource Management Charts
// --------------------------
function showResourceChart(
	elementId,
	chartType,
	chartTitle,
	xlabels,
	yData,
	isLegend = true,
	suffix
) {
	const chart = document.getElementById(elementId);
	if (newResourceChart !== null) {
		newResourceChart.destroy();
	}
	newResourceChart = new Chart(chart, {
		type: chartType,
		data: {
			labels: xlabels,
			datasets: [
				{
					data: yData,
					backgroundColor,
					borderColor,
					borderWidth: 1,
				},
			],
		},

		options: {
			plugins: {
				legend: {
					display: isLegend,
				},
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
				datalabels: {
					anchor: "end",
					formatter: (value, ctx) => {
						return value + suffix;
					},
				},
			},
		},
		plugins: [ChartDataLabels],
	});
}

async function showResourceUtilizationRateChart() {
	const response_data = await getData("/api/resource-management");

	const resourceNames = response_data.map((item) => item.resource_name);
	const utilizationRates = response_data.map((item) => item.utilization_rate);

	showResourceChart(
		"resourceManagementChart",
		"polarArea",
		"Resource Utilization Rates",
		resourceNames,
		utilizationRates,
		true,
		"%"
	);
}

async function showResourceAllocationTeacherNumbersChart() {
	const response_data = await getData("/api/resource-management");

	const resourceNames = response_data.map((item) => item.resource_name);
	const allocatedTeacherNumbers = response_data.map(
		(item) => item.allocated_teachers.length
	);

	showResourceChart(
		"resourceManagementChart",
		"pie",
		"Resource Allocated Teacher Numbers",
		resourceNames,
		allocatedTeacherNumbers,
		true,
		""
	);
}

function showResourceMangementChart(value) {
	if (value === "resourceUtilizationRatesChart") {
		showResourceUtilizationRateChart();
	} else if (value === "resourceAllocatedTeacherNumbersChart") {
		showResourceAllocationTeacherNumbersChart();
	}
}

showResourceMangementChart("resourceUtilizationRatesChart");

//
//
// Coach Teacher Interactions Chart
function showCoachTeacherChart(
	elementId,
	chartType,
	chartTitle,
	xlabels,
	yData
) {
	const chart = document.getElementById(elementId);

	new Chart(chart, {
		type: chartType,
		data: {
			labels: xlabels,
			datasets: [
				{
					data: yData,
					backgroundColor,
					borderColor,
					borderWidth: 1,
				},
			],
		},

		options: {
			plugins: {
				legend: {
					display: true,
				},
				title: {
					display: true,
					text: chartTitle,
					font: {
						size: 20,
					},
				},
			},
		},
	});
}

async function showCoachTeacherInteractionsChart() {
	const response_data = await getData("/api/coach-teacher");

	/** coach_summary = {"Emily Turner": 2,
						 "Michael Rodriguez": 2}
	 */
	const coach_summary = response_data.reduce((aggregate, item) => {
		if (!aggregate[item.coach_name]) {
			aggregate[item.coach_name] = 0;
		}
		aggregate[item.coach_name] += 1;
		return aggregate;
	}, {});

	const coachNames = Object.keys(coach_summary);
	const teacherNumbers = Object.values(coach_summary);

	showCoachTeacherChart(
		"coachTeacherChart",
		"polarArea",
		"Coach Teacher Interactions Numbers",
		coachNames,
		teacherNumbers
	);
}

showCoachTeacherInteractionsChart();

import { error } from '@sveltejs/kit';

export async function load({ params }) {
    console.log("Running load....");
    console.log("params:", params); // Debugging: Log the params to ensure the title is captured
    const title = params.title;

    // Simulate fetching data based on the title
    const exams = [
        {
            name: 'AWS Certified Solutions Architect',
            icon: '🖥️',
            title: 'aws-certified-solutions-architect', // Make sure the path matches the dynamic route
            length: 200,
            lastUpdated: '2024-06-01'
        },
        {
            name: 'Google Cloud Professional Data Engineer',
            icon: '☁️',
            title: 'google-cloud-professional-data-engineer', // Make sure the path matches the dynamic route
            length: 180,
            lastUpdated: '2024-05-15'
        },
        {
            name: 'Microsoft Certified: Azure Fundamentals',
            icon: '🔧',
            title: 'microsoft-certified-azure-fundamentals', // Make sure the path matches the dynamic route
            length: 220,
            lastUpdated: '2024-04-20'
        }
    ];

    const exam = exams.find(e => e.title === title);
    console.log("exam:", exam); // Debugging: Log the exam data to ensure it is found

    if (!exam) {
        throw error(404, 'Exam not found');
    }

    return {
        exam
    };
}

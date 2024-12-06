import DeckOneImage from "../../assets/deck-1.png";
import DeckTwoImage from "../../assets/deck-2.png";
import DeckThreeImage from "../../assets/deck-3.png";

export const demoDeckDetails = {
	description:
		"Lorem ipsum odor amet, consectetuer adipiscing elit. Sapien turpis velit bibendum habitasse, phasellus est luctus dignissim. Non faucibus cubilia in phasellus mus ligula luctus cursus ante. Rutrum at blandit a pharetra rhoncus tristique facilisis. Ridiculus vitae quis cras cras luctus rhoncus nulla torquent. Pellentesque per varius vestibulum, ullamcorper semper habitant id ipsum. Turpis tempor pulvinar leo ex nam ut potenti. Luctus natoque gravida finibus sed ullamcorper conubia inceptos arcu.",
	modules: [
		{
			id: "1",
			name: "Learn",
			description:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
			sections: 12,
			questions: 140,
			completeWeeksTime: 2,
		},
		{
			id: "2",
			name: "Understand",
			description:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
			sections: 12,
			questions: 130,
			completeWeeksTime: 2,
		},
		{
			id: "3",
			name: "Apply",
			description:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
			sections: 9,
			questions: 108,
			completeWeeksTime: 2,
		},
	],
};

export const DUMMY_CARDS = [
	{
		image: DeckOneImage,
		id: "test1",
		lastUpdated: "2024-06-01T07:00:00.898000+00:00",
		length: 200,
		name: "AWS Certified Solutions Architect",
	},
	{
		image: DeckTwoImage,
		id: "test2",
		lastUpdated: "2024-05-15T07:00:00.518000+00:00",
		length: 180,
		name: "Exam Title",
	},
	{
		image: DeckThreeImage,
		id: "test3",
		lastUpdated: "2024-04-20T07:00:00.177000+00:00",
		length: 220,
		name: "Microsoft Certified: Azure Fundamentals",
	},
];

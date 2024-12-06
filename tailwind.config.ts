import { join } from "path";
import type { Config } from "tailwindcss";
import forms from "@tailwindcss/forms";
import typography from "@tailwindcss/typography";
import { skeleton } from "@skeletonlabs/tw-plugin";

export default {
	darkMode: "class",
	content: [
		"./src/**/*.{html,js,svelte,ts}",
		join(
			require.resolve("@skeletonlabs/skeleton"),
			"../**/*.{html,js,svelte,ts}"
		),
	],
	theme: {
		extend: {
			screens: {
				"2.5xl": "1640px",
				"3xl": "1750px",
			},
			fontFamily: {
				inter: ["Inter", "sans-serif"],
				roboto: ["Roboto", "sans-serif"],
			},
			borderRadius: {
				"4xl": "32px",
			},
			colors: {
				primary: {
					900: "#1E3A8A",
					800: "#1E40AF",
					700: "#1D4ED8",
					600: "#2563EB",
					500: "#3B82F6",
					400: "#60A5FA",
					300: "#93C5FD",
					200: "#BFDBFE",
					100: "#DBEAFE",
					50: "#EFF6FF",
				},
				secondary: {
					1100: "#032419",
					1000: "#043726",
					900: "#075B3F",
					800: "#09704D",
					700: "#0B8C61",
					600: "#0EA774",
					500: "#0FBA81",
					400: "#57CFA7",
					300: "#9FE3CD",
					200: "#C3EEE0",
					100: "#CFF1E6",
					50: "#DBF5EC",
				},
				tertiary: {
					900: "#1B0D42",
					800: "#2A175F",
					700: "#39227C",
					600: "#4B2F9A",
					500: "#5E3EB7",
					400: "#7250D4",
					300: "#8863F1",
					200: "#B196FF",
					100: "#D2C3FF",
					50: "#F4F0FF",
				},
				error: {
					900: "#680C3A",
					800: "#7F0F47",
					700: "#9F1359",
					600: "#BF176A",
					500: "#D41976",
					400: "#E15E9F",
					300: "#EEA3C8",
					200: "#F4C6DD",
					100: "#F6D1E4",
					50: "#F9DDEA",
				},
				interface: {
					900: "#111827",
					800: "#1F2937",
					700: "#374151",
					600: "#4B5563",
					500: "#6B7280",
					400: "#9CA3AF",
					300: "#D1D5DB",
					200: "#E5E7EB",
					100: "#F4F5F7",
					50: "#FAFAFA",
				},
			},
		},
	},
	plugins: [
		forms,
		typography,
		skeleton({
			themes: {
				preset: [
					{
						name: "wintry",
						enhancements: true,
					},
					{
						name: "crimson",
						enhancements: true,
					},
				],
			},
		}),
	],
} satisfies Config;

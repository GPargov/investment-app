/** @format */

import React, { useState } from "react";
import axios from "axios";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	Legend,
	ResponsiveContainer,
} from "recharts";

function App() {
	const [form, setForm] = useState({
		initial: 10000,
		monthly: 500,
		years: 30,
		rate: 10,
		inflation: 2.5,
	});

	const [result, setResult] = useState<{
		nominal: number;
		real: number;
		yearly_values: {
			year: number;
			nominal: number;
			real: number;
		}[];
	} | null>(null);

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setForm({ ...form, [e.target.name]: e.target.value });
	};

	const handleSubmit = async () => {
		const payload = {
			initial: parseFloat(form.initial as any),
			monthly: parseFloat(form.monthly as any),
			years: parseInt(form.years as any),
			rate: parseFloat(form.rate as any),
			inflation: parseFloat(form.inflation as any),
		};
		const res = await axios.post(
			"http://localhost:8000/api/calculate/",
			payload
		);
		setResult(res.data);
	};

	return (
		<div style={{ padding: 20 }}>
			<h2>Investment Calculator</h2>
			<input
				name="initial"
				type="number"
				placeholder="Initial Investment"
				onChange={handleChange}
				value={form.initial}
			/>
			<br />
			<input
				name="monthly"
				type="number"
				placeholder="Monthly Contribution"
				onChange={handleChange}
				value={form.monthly}
			/>
			<br />
			<input
				name="years"
				type="number"
				placeholder="Years"
				onChange={handleChange}
				value={form.years}
			/>
			<br />
			<input
				name="rate"
				type="number"
				placeholder="Expected Annual Return (%)"
				onChange={handleChange}
				value={form.rate}
			/>
			<br />
			<input
				name="inflation"
				type="number"
				placeholder="Inflation Rate (%)"
				onChange={handleChange}
				value={form.inflation}
			/>
			<br />
			<button onClick={handleSubmit}>Calculate</button>
			{result?.yearly_values && (
				<div style={{ width: "100%", height: 400 }}>
					<h3>Investment Growth Over Time</h3>
					<ResponsiveContainer>
						<LineChart data={result.yearly_values}>
							<CartesianGrid strokeDasharray="3 3" />
							<XAxis dataKey="year" />
							<YAxis />
							<Tooltip />
							<Legend />
							<Line
								type="monotone"
								dataKey="nominal"
								stroke="#8884d8"
								name="Nominal Value"
							/>
							<Line
								type="monotone"
								dataKey="real"
								stroke="#82ca9d"
								name="Real Value (Inflation-Adjusted)"
							/>
						</LineChart>
					</ResponsiveContainer>
				</div>
			)}
		</div>
	);
}

export default App;

"use client";
import React from 'react';
import { useQuery } from '@tanstack/react-query';

const graphqlEndpoint = 'http://localhost:8000/api/graphql/'; // Use the proxy setup in next.config.mjs

// Fetch data function using fetch API
const fetchData = async () => {
  console.log('Fetching data from GraphQL endpoint:', graphqlEndpoint);
  const response = await fetch(graphqlEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      "query": "query GetAllSubscriptionsInfo { allSubscriptionsInfo { id service time } }"
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch subscriptions: ${response.statusText}`);
  }

  const data = await response.json();
  console.log('Response:', data);
  return data.data.allSubscriptionsInfo; // Return the subscription data from the GraphQL response
};

function SubscriptionListPage() {
  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['subscriptions'],
    queryFn: fetchData, // Use the fetchData function here
  });

  if (isLoading) {
    return <div>Loading subscriptions...</div>;
  }

  if (isError) {
    return <div>Error loading subscriptions: {error.message}</div>;
  }

  if (!data || data.length === 0) {
    return <div>No Subscriptions found.</div>;
  }

  return (
    <div>
      <h1>Subscription List</h1>
      <ul>
        {data.map((subscriptions) => (
          <li key={subscriptions.id}>
            Service: {subscriptions.service}, Time: {subscriptions.time}, ID: {subscriptions.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SubscriptionListPage;
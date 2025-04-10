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
      "query": "query GetAllUsersInfo { allUsersInfo { id email name } }"
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch users: ${response.statusText}`);
  }

  const data = await response.json();
  console.log('Response:', data);
  return data.data.allUsersInfo; // Return the user data from the GraphQL response
};

function UserListPage() {
  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchData, // Use the fetchData function here
  });

  if (isLoading) {
    return <div>Loading users...</div>;
  }

  if (isError) {
    return <div>Error loading users: {error.message}</div>;
  }

  if (!data || data.length === 0) {
    return <div>No users found.</div>;
  }

  return (
    <div>
      <h1>User List</h1>
      <ul>
        {data.map((user) => (
          <li key={user.id}>
            {user.name} ({user.email}) - ID: {user.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserListPage;
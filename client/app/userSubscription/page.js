"use client";
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { request } from 'graphql-request';

const graphqlEndpoint = 'http://localhost:8000/api/graphql/';  

const GET_USER_SUBSCRIPTIONS = `
  query GetAllUserSubscriptions {
    allUsersubscriptionsInfo {
    id
      user {
        id
        email
        name
      }
      subscription {
        id
        service
      }
    }
  }
`;

function UserSubscriptions() {
  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['userSubscriptions'],
    queryFn: async () => {
      const response = await request(graphqlEndpoint, GET_USER_SUBSCRIPTIONS);
      return response.allUsersubscriptionsInfo;
    },
  });

  if (isLoading) {
    return <div>Loading user subscriptions...</div>;
  }

  if (isError) {
    return <div>Error loading user subscriptions: {error.message}</div>;
  }

  if (!data) {
    return <div>No user subscriptions found.</div>;
  }

  return (
    <div>
      <h1>User Subscriptions</h1>
      <ul>
        {data.map((item) => (
          <li key={item.id}>
            User: {item.user.name} ({item.user.email}) - Subscription: {item.subscription.service}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserSubscriptions;
/**
 * API Utility Module
 * Handles all API calls with JWT token management
 */

const API = (() => {
	const API_BASE = 'http://localhost:8000/api';
	const TOKEN_KEY = 'auth_token';
	const USER_KEY = 'current_user';

	/**
	 * Store the auth token in localStorage
	 */
	const setToken = (token) => {
		localStorage.setItem(TOKEN_KEY, token);
	};

	/**
	 * Retrieve the auth token from localStorage
	 */
	const getToken = () => {
		return localStorage.getItem(TOKEN_KEY);
	};

	/**
	 * Clear the auth token from localStorage
	 */
	const clearToken = () => {
		localStorage.removeItem(TOKEN_KEY);
		localStorage.removeItem(USER_KEY);
	};

	/**
	 * Store the current user in localStorage
	 */
	const setUser = (user) => {
		localStorage.setItem(USER_KEY, JSON.stringify(user));
	};

	/**
	 * Get the current user from localStorage
	 */
	const getUser = () => {
		const user = localStorage.getItem(USER_KEY);
		return user ? JSON.parse(user) : null;
	};

	/**
	 * Check if user is authenticated
	 */
	const isAuthenticated = () => {
		return !!getToken();
	};

	/**
	 * Make an authenticated API call
	 */
	const call = async (endpoint, options = {}) => {
		const url = `${API_BASE}${endpoint}`;
		const token = getToken();

		const headers = {
			'Content-Type': 'application/json',
			...options.headers
		};

		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
		}

		const config = {
			...options,
			headers
		};

		try {
			const response = await fetch(url, config);
			const data = await response.json();

			if (!response.ok) {
				throw new Error(data.detail || `API Error: ${response.status}`);
			}

			return data;
		} catch (error) {
			console.error('API Error:', error);
			throw error;
		}
	};

	/**
	 * Login endpoint
	 */
	const login = async (username, password) => {
		try {
			const data = await call('/login', {
				method: 'POST',
				body: JSON.stringify({ username, password })
			});

			setToken(data.access_token);
			setUser(data.user);

			return data;
		} catch (error) {
			console.error('Login failed:', error);
			throw error;
		}
	};

	/**
	 * Logout endpoint
	 */
	const logout = async () => {
		try {
			const token = getToken();
			if (token) {
				await call('/logout', {
					method: 'POST',
					headers: {
						'Authorization': `Bearer ${token}`
					}
				});
			}
		} catch (error) {
			console.error('Logout error:', error);
		} finally {
			clearToken();
		}
	};

	/**
	 * Get current user info
	 */
	const getCurrentUser = async () => {
		try {
			const data = await call('/me', {
				method: 'GET'
			});
			setUser(data);
			return data;
		} catch (error) {
			console.error('Failed to get current user:', error);
			throw error;
		}
	};

	/**
	 * Get all items from a model
	 */
	const getAll = async (modelName) => {
		return call(`/${modelName}`, { method: 'GET' });
	};

	/**
	 * Get a single item
	 */
	const getOne = async (modelName, id) => {
		return call(`/${modelName}/${id}`, { method: 'GET' });
	};

	/**
	 * Create a new item
	 */
	const create = async (modelName, data) => {
		return call(`/${modelName}`, {
			method: 'POST',
			body: JSON.stringify(data)
		});
	};

	/**
	 * Update an item
	 */
	const update = async (modelName, id, data) => {
		return call(`/${modelName}/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		});
	};

	/**
	 * Delete an item
	 */
	const remove = async (modelName, id) => {
		return call(`/${modelName}/${id}`, { method: 'DELETE' });
	};

	return {
		call,
		login,
		logout,
		getCurrentUser,
		getAll,
		getOne,
		create,
		update,
		remove,
		setToken,
		getToken,
		clearToken,
		setUser,
		getUser,
		isAuthenticated
	};
})();

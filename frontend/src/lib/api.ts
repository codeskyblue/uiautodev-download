// Types
export interface FileInfo {
	name: string;
	size: number;
	download_url: string;
}

export interface VersionDetail {
	version: string;
	files: FileInfo[];
}

export interface VersionsList {
	versions: string[];
}

// API Functions
export async function fetchVersions(): Promise<string[]> {
	const response = await fetch('/api/versions', {
		signal: AbortSignal.timeout(10000)
	});
	if (!response.ok) {
		throw new Error(`Failed to fetch versions: ${response.statusText}`);
	}
	const data: VersionsList = await response.json();
	return data.versions;
}

export async function fetchVersionDetail(version: string): Promise<VersionDetail> {
	const response = await fetch(`/api/versions/${encodeURIComponent(version)}`, {
		signal: AbortSignal.timeout(10000)
	});
	if (!response.ok) {
		throw new Error(`Failed to fetch version detail: ${response.statusText}`);
	}
	return response.json();
}

// Helper: Format file size
export function formatFileSize(bytes: number): string {
	if (bytes === 0) return '-';
	const units = ['B', 'KB', 'MB', 'GB'];
	const k = 1024;
	const i = Math.floor(Math.log(bytes) / Math.log(k));
	return `${(bytes / Math.pow(k, i)).toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

// Helper: Detect platform from filename
export function detectPlatform(filename: string): { platform: string; icon: string } {
	const lower = filename.toLowerCase();

	if (lower.includes('mac') || lower.includes('darwin') || lower.includes('applesilicon')) {
		return { platform: 'macOS', icon: 'Apple' };
	}
	if (lower.includes('win') || lower.includes('.exe')) {
		return { platform: 'Windows', icon: 'Monitor' };
	}
	if (lower.includes('linux')) {
		return { platform: 'Linux', icon: 'Terminal' };
	}
	return { platform: 'Other', icon: 'File' };
}

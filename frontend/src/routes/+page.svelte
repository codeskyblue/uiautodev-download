<script lang="ts">
	import { onMount } from 'svelte';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import * as Table from '$lib/components/ui/table';
	import { fetchVersions, fetchVersionDetail, formatFileSize, detectPlatform, type FileInfo } from '$lib/api';
	import { resolve } from '$app/paths';

	let latestVersion = $state<string>('');
	let files = $state<FileInfo[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			const versions = await fetchVersions();
			if (versions.length > 0) {
				latestVersion = versions[0];
				const detail = await fetchVersionDetail(latestVersion);
				files = detail.files.filter((f) => f.size > 0); // Filter out folder entries
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load data';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>UIAuto.dev - Download</title>
	<meta name="description" content="Download UIAuto.dev - Mobile UI Automation Tool" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-background to-muted/20">
	<header class="border-b bg-background/80 backdrop-blur-sm sticky top-0 z-50">
		<div class="container mx-auto px-4 py-4 flex items-center justify-between">
			<div class="flex items-center gap-3">
				<div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
					<span class="text-primary-foreground font-bold text-sm">U</span>
				</div>
				<h1 class="text-xl font-semibold">UIAuto.dev</h1>
			</div>
			<nav class="flex items-center gap-4">
				<a href={resolve('/')} class="text-sm font-medium text-foreground">Download</a>
				<a href={resolve('/history')} class="text-sm text-muted-foreground hover:text-foreground transition-colors">History</a>
				<a href="https://uiauto.dev" target="_blank" rel="noopener noreferrer" class="text-sm text-muted-foreground hover:text-foreground transition-colors">Docs</a>
			</nav>
		</div>
	</header>

	<main class="container mx-auto px-4 py-12">
		<div class="max-w-4xl mx-auto space-y-8">
			<!-- Hero Section -->
			<section class="text-center space-y-4">
				<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
					<span class="relative flex h-2 w-2">
						<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
						<span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
					</span>
					Latest Release
				</div>
				<h2 class="text-4xl md:text-5xl font-bold tracking-tight">Mobile UI Automation</h2>
				<p class="text-lg text-muted-foreground max-w-2xl mx-auto">
					Powerful automation tools for mobile testing. Download the latest version and get started
					today.
				</p>
				{#if latestVersion}
					<Badge variant="outline" class="text-base px-3 py-1">v{latestVersion}</Badge>
				{/if}
			</section>

			{#if loading}
				<div class="text-center py-12">
					<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
					<p class="mt-4 text-muted-foreground">Loading downloads...</p>
				</div>
			{:else if error}
				<Card>
					<CardContent class="py-8">
						<p class="text-destructive text-center">Failed to load: {error}</p>
					</CardContent>
				</Card>
			{:else}
				<!-- Downloads Section -->
				<section class="space-y-4">
					<Card>
						<CardHeader>
							<CardTitle>Downloads</CardTitle>
							<CardDescription>Select your platform to download</CardDescription>
						</CardHeader>
						<CardContent>
							<Table.Root>
								<Table.Header>
									<Table.Row>
										<Table.Head>Platform</Table.Head>
										<Table.Head>File</Table.Head>
										<Table.Head class="text-right">Size</Table.Head>
										<Table.Head class="text-right">Download</Table.Head>
									</Table.Row>
								</Table.Header>
								<Table.Body>
									{#each files as file (file.name)}
										{@const platform = detectPlatform(file.name)}
										<Table.Row>
											<Table.Cell>
												<Badge variant="secondary">{platform.platform}</Badge>
											</Table.Cell>
											<Table.Cell class="font-mono text-sm">{file.name}</Table.Cell>
											<Table.Cell class="text-right text-muted-foreground">{formatFileSize(file.size)}</Table.Cell>
											<Table.Cell class="text-right">
												<a
													href={file.download_url}
													download
													class="inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 shadow-xs h-8 px-3"
												>
													Download
												</a>
											</Table.Cell>
										</Table.Row>
									{/each}
								</Table.Body>
							</Table.Root>
						</CardContent>
					</Card>
				</section>

				<!-- Links Section -->
				<section class="flex flex-wrap gap-4 justify-center">
					<a href={resolve('/history')} class="text-sm text-muted-foreground hover:text-foreground transition-colors">
						View all versions →
					</a>
				</section>
			{/if}
		</div>
	</main>

	<footer class="border-t mt-16">
		<div class="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
			<p>© 2024 UIAuto.dev. All rights reserved.</p>
		</div>
	</footer>
</div>

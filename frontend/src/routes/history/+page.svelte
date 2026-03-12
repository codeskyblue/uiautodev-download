<script lang="ts">
	import { onMount } from 'svelte';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import * as Table from '$lib/components/ui/table';
	import { fetchVersions, fetchVersionDetail, formatFileSize, detectPlatform, type FileInfo } from '$lib/api';
	import { SvelteSet } from 'svelte/reactivity';
	import { resolve } from '$app/paths';

	interface VersionWithFiles {
		version: string;
		files: FileInfo[];
	}

	let versions = $state<VersionWithFiles[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let expandedVersions = new SvelteSet<string>();

	function toggleVersion(version: string) {
		if (expandedVersions.has(version)) {
			expandedVersions.delete(version);
		} else {
			expandedVersions.add(version);
		}
	}

	onMount(async () => {
		try {
			const versionList = await fetchVersions();
			// Load details for all versions
			versions = await Promise.all(
				versionList.map(async (v) => {
					const detail = await fetchVersionDetail(v);
					return {
						version: v,
						files: detail.files.filter((f) => f.size > 0)
					};
				})
			);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load versions';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>UIAuto.dev - Version History</title>
	<meta name="description" content="Browse all versions of UIAuto.dev" />
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
				<a href={resolve('/')} class="text-sm text-muted-foreground hover:text-foreground transition-colors">Download</a>
				<a href={resolve('/history')} class="text-sm font-medium text-foreground">History</a>
				<a href="https://uiauto.dev" target="_blank" rel="noopener noreferrer" class="text-sm text-muted-foreground hover:text-foreground transition-colors">Docs</a>
			</nav>
		</div>
	</header>

	<main class="container mx-auto px-4 py-12">
		<div class="max-w-5xl mx-auto space-y-8">
			<!-- Header Section -->
			<section class="space-y-2">
				<h2 class="text-3xl md:text-4xl font-bold tracking-tight">Version History</h2>
				<p class="text-muted-foreground">Browse and download all available versions</p>
			</section>

			{#if loading}
				<div class="text-center py-12">
					<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
					<p class="mt-4 text-muted-foreground">Loading versions...</p>
				</div>
			{:else if error}
				<Card>
					<CardContent class="py-8">
						<p class="text-destructive text-center">Failed to load: {error}</p>
					</CardContent>
				</Card>
			{:else}
				<!-- Version List -->
				<div class="space-y-4">
					{#each versions as item (item.version)}
						{@const isExpanded = expandedVersions.has(item.version)}
						{@const isLatest = item.version === versions[0]?.version}
						<Card class={isLatest ? 'border-primary' : ''}>
							<button
								onclick={() => toggleVersion(item.version)}
								class="w-full text-left"
								type="button"
							>
								<CardHeader class="flex flex-row items-center justify-between py-4 px-6">
									<div class="flex items-center gap-3">
										<span class="text-muted-foreground">
											{#if isExpanded}
												<svg
													xmlns="http://www.w3.org/2000/svg"
													width="20"
													height="20"
													viewBox="0 0 24 24"
													fill="none"
													stroke="currentColor"
													stroke-width="2"
													stroke-linecap="round"
													stroke-linejoin="round"
												><path d="m6 9 6 6 6-6"/></svg>
											{:else}
												<svg
													xmlns="http://www.w3.org/2000/svg"
													width="20"
													height="20"
													viewBox="0 0 24 24"
													fill="none"
													stroke="currentColor"
													stroke-width="2"
													stroke-linecap="round"
													stroke-linejoin="round"
												><path d="m9 18 6-6-6-6"/></svg>
											{/if}
										</span>
										<div class="flex items-center gap-2">
											<span class="font-semibold">v{item.version}</span>
											{#if isLatest}
												<Badge variant="default" class="text-xs">Latest</Badge>
											{/if}
										</div>
										<span class="text-sm text-muted-foreground"
											>{item.files.length} file{item.files.length === 1 ? '' : 's'}</span
										>
									</div>
									<span class="text-sm text-muted-foreground">
										{isExpanded ? 'Collapse' : 'Expand'}
									</span>
								</CardHeader>
							</button>

							{#if isExpanded}
								<CardContent class="pt-0 px-6 pb-4">
									<Table.Root>
										<Table.Header>
											<Table.Row>
												<Table.Head class="w-[100px]">Platform</Table.Head>
												<Table.Head>File</Table.Head>
												<Table.Head class="text-right w-[100px]">Size</Table.Head>
												<Table.Head class="text-right w-[100px]">Download</Table.Head>
											</Table.Row>
										</Table.Header>
										<Table.Body>
											{#each item.files as file (file.name)}
												{@const platform = detectPlatform(file.name)}
												<Table.Row>
													<Table.Cell>
														<Badge variant="secondary" class="text-xs">{platform.platform}</Badge>
													</Table.Cell>
													<Table.Cell class="font-mono text-sm">{file.name}</Table.Cell>
													<Table.Cell class="text-right text-muted-foreground text-sm">
														{formatFileSize(file.size)}
													</Table.Cell>
													<Table.Cell class="text-right">
														<a
															href={file.download_url}
															download
															class="inline-flex items-center justify-center rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 shadow-xs h-7 px-3 text-xs"
														>
															Download
														</a>
													</Table.Cell>
												</Table.Row>
											{/each}
										</Table.Body>
									</Table.Root>
								</CardContent>
							{/if}
						</Card>
					{/each}
				</div>
			{/if}
		</div>
	</main>

	<footer class="border-t mt-16">
		<div class="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
			<p>© 2024 UIAuto.dev. All rights reserved.</p>
		</div>
	</footer>
</div>

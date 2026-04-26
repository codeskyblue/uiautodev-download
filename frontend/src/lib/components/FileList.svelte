<script lang="ts">
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import * as Table from '$lib/components/ui/table';
	import { Button } from "$lib/components/ui/button/index.js";
	import { formatFileSize, detectPlatform, type FileInfo } from '$lib/api';

	interface Props {
		files: FileInfo[];
	}

	let { files }: Props = $props();

	let copiedUrl = $state('');

	async function copyLink(url: string) {
		await navigator.clipboard.writeText(url);
		copiedUrl = url;
		setTimeout(() => { copiedUrl = ''; }, 2000);
	}

	// 分为桌面版和服务器版
	let desktopFiles = $derived(files.filter(f => f.name.endsWith('.dmg') || f.name.endsWith('.zip')));
	let serverFiles = $derived(files.filter(f => f.name.toLowerCase().includes('server')));
</script>

{#if desktopFiles.length > 0}
	<Card>
		<CardHeader>
			<CardTitle>Desktop Version</CardTitle>
			<CardDescription>Download for macOS and Windows</CardDescription>
		</CardHeader>
		<CardContent>
			<Table.Root>
				<Table.Header>
					<Table.Row>
						<Table.Head>Platform</Table.Head>
						<Table.Head>File</Table.Head>
						<Table.Head class="text-right">Size</Table.Head>
						<Table.Head class="text-right">Actions</Table.Head>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#each desktopFiles as file (file.name)}
						{@const platform = detectPlatform(file.name)}
						<Table.Row>
							<Table.Cell>
								<Badge variant="secondary">{platform.platform}</Badge>
							</Table.Cell>
							<Table.Cell class="font-mono text-sm">{file.name}</Table.Cell>
							<Table.Cell class="text-right text-muted-foreground">{formatFileSize(file.size)}</Table.Cell>
							<Table.Cell class="text-right">
								<div class="inline-flex items-center gap-2">
									<Button
										variant="outline"
										onclick={() => copyLink(file.download_url)}
									>
										{#if copiedUrl === file.download_url}
											Copied
										{:else}
											Copy
										{/if}
									</Button>
									<a
										href={file.download_url}
										download
										rel="external"
										class="inline-flex items-center justify-center rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] bg-primary text-primary-foreground hover:bg-primary/90 shadow-xs h-8 px-3"
									>
										Download
									</a>
								</div>
							</Table.Cell>
						</Table.Row>
					{/each}
				</Table.Body>
			</Table.Root>
		</CardContent>
	</Card>
{/if}

{#if serverFiles.length > 0}
	<Card>
		<CardHeader>
			<CardTitle>Server Version</CardTitle>
			<CardDescription>Download for CI/CD and server environments</CardDescription>
		</CardHeader>
		<CardContent>
			<Table.Root>
				<Table.Header>
					<Table.Row>
						<Table.Head>Platform</Table.Head>
						<Table.Head>File</Table.Head>
						<Table.Head class="text-right">Size</Table.Head>
						<Table.Head class="text-right">Actions</Table.Head>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#each serverFiles as file (file.name)}
						{@const platform = detectPlatform(file.name)}
						<Table.Row>
							<Table.Cell>
								<Badge variant="secondary">{platform.platform}</Badge>
							</Table.Cell>
							<Table.Cell class="font-mono text-sm">{file.name}</Table.Cell>
							<Table.Cell class="text-right text-muted-foreground">{formatFileSize(file.size)}</Table.Cell>
							<Table.Cell class="text-right">
								<div class="inline-flex items-center gap-2">
									<button
										type="button"
										onclick={() => copyLink(file.download_url)}
										class="inline-flex items-center justify-center rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] border border-input bg-background hover:bg-accent hover:text-accent-foreground h-8 px-3 cursor-pointer"
									>
										{#if copiedUrl === file.download_url}
											Copied!
										{:else}
											Copy Link
										{/if}
									</button>
									<a
										href={file.download_url}
										download
										rel="external"
										class="inline-flex items-center justify-center rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] bg-primary text-primary-foreground hover:bg-primary/90 shadow-xs h-8 px-3"
									>
										Download
									</a>
								</div>
							</Table.Cell>
						</Table.Row>
					{/each}
				</Table.Body>
			</Table.Root>
		</CardContent>
	</Card>
{/if}

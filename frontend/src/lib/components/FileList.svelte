<script lang="ts">
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import * as Table from '$lib/components/ui/table';
	import { formatFileSize, detectPlatform, type FileInfo } from '$lib/api';

	interface Props {
		files: FileInfo[];
	}

	let { files }: Props = $props();

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
						<Table.Head class="text-right">Download</Table.Head>
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
								<a
									href={file.download_url}
									download
									rel="noopener noreferrer"
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
						<Table.Head class="text-right">Download</Table.Head>
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
								<a
									href={file.download_url}
									download
									rel="noopener noreferrer"
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
{/if}
